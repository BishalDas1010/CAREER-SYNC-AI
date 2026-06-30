# ats_analyzer.py
import os
import json
from dotenv import load_dotenv
from textLoader.ResumeLoader import ResumeLoader
from textLoader.docs_loader import docs_loader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI
import tempfile
import shutil

load_dotenv()

class ATSService:
    def __init__(self):
        # Configuration
        self.EMBEDDING_MODEL = "all-MiniLM-L6-v2"
        self.CHUNK_SIZE = 500
        self.CHUNK_OVERLAP = 100
        self.RETRIEVER_K = 5
        self.MMR_LAMBDA_RESUME = 0.9
        self.MMR_LAMBDA_JOB = 0.8

        # Per‑session state
        self.embedding_model = None
        self.resume_vectorstore = None
        self.job_vectorstore = None
        self.resume_context = None
        self.job_context = None
        self.llm = None

        # Load embedding model on init
        self._load_embedding_model()

    def _load_embedding_model(self):
        """Load HuggingFace embeddings (GPU if available)."""
        try:
            model = HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL,
                model_kwargs={'device': 'cuda'}
            )
            _ = model.embed_query("test")
            print("Embedding model loaded on GPU.")
            self.embedding_model = model
        except Exception:
            print("CUDA not available, falling back to CPU.")
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )

    def _text_splitter(self):
        return RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.CHUNK_OVERLAP
        )

    def process_resume(self, resume_bytes: bytes) -> None:
        """
        Accept resume PDF as bytes, save temporarily, index, and store vectorstore.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume_bytes)
                tmp_path = tmp.name

            splitter = self._text_splitter()
            loader = ResumeLoader(tmp_path, self.embedding_model)
            docs = loader.pdf_loader()
            chunks = loader.text_splitter(docs, splitter)
            self.resume_vectorstore = loader.vector_store(chunks, self.embedding_model)

            os.unlink(tmp_path)
            print("Resume processed and indexed.")
        except Exception as e:
            raise RuntimeError(f"Error processing resume: {e}")

    def process_job_description(self, job_bytes: bytes) -> None:
        """
        Accept job description (TXT) as bytes, save temporarily, index, and store vectorstore.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(job_bytes)
                tmp_path = tmp.name

            splitter = self._text_splitter()
            loader = docs_loader(tmp_path, self.embedding_model)
            docs = loader.pdf_loader()   # This method should handle .txt as well
            chunks = loader.text_splitter(docs, splitter)
            self.job_vectorstore = loader.vector_store(chunks, self.embedding_model)

            os.unlink(tmp_path)
            print("Job description processed and indexed.")
        except Exception as e:
            raise RuntimeError(f"Error processing job description: {e}")

    def retrieve_chunks(self) -> None:
        """Use MMR to extract relevant chunks from both documents."""
        resume_query = """
        Extract the candidate's skills, technical expertise,
        projects, work experience, education,
        certifications, achievements, and relevant keywords.
        """
        job_query = """
        What skills, qualifications, experience, responsibilities,
        and technologies are required for this job?
        """

        resume_retriever = self.resume_vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": self.RETRIEVER_K, "lambda_mult": self.MMR_LAMBDA_RESUME}
        )
        job_retriever = self.job_vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": self.RETRIEVER_K, "lambda_mult": self.MMR_LAMBDA_JOB}
        )

        retrieved_resume = resume_retriever.invoke(resume_query)
        retrieved_job = job_retriever.invoke(job_query)

        if not retrieved_resume or not retrieved_job:
            raise RuntimeError("No relevant chunks retrieved. Check document content.")

        self.resume_context = "\n\n".join([doc.page_content for doc in retrieved_resume])
        self.job_context = "\n\n".join([doc.page_content for doc in retrieved_job])
        print("Relevant chunks retrieved.")

    def load_llm(self):
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0.3)

    def _get_recommendation(self) -> dict:
        """
        Ask the LLM to produce a structured final recommendation.
        Returns a dict with keys: shortlist, score, reasons, upskill_plan, alternative_roles.
        """
        rec_prompt = f"""
        You are an expert ATS resume reviewer. Based on the following Job Description and Candidate Resume,
        produce a final recommendation in **valid JSON only**, with these exact keys:

        - "shortlist": boolean (true if the candidate should be shortlisted, false otherwise)
        - "score": integer (0-100) representing the overall match percentage
        - "reasons": list of strings, each explaining a key reason for the verdict
        - "upskill_plan": string, a concise plan for the candidate to improve (if not shortlisted)
        - "alternative_roles": list of strings, suggested alternative job titles if not a good fit

        **Job Description:**
        {self.job_context}

        **Candidate Resume:**
        {self.resume_context}

        Return **only** the JSON object, no other text.
        """

        try:
            response = self.llm.invoke(rec_prompt)
            raw = response.content.strip()
            # Remove any markdown code fences if present
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.endswith("```"):
                raw = raw[:-3]
            rec_data = json.loads(raw)
            # Ensure all keys exist
            required_keys = {"shortlist", "score", "reasons", "upskill_plan", "alternative_roles"}
            if not required_keys.issubset(rec_data.keys()):
                raise ValueError("Missing required keys in JSON")
            return rec_data
        except Exception as e:
            # Fallback: return a sensible default based on common patterns
            print(f"Could not parse recommendation JSON: {e}. Using fallback.")
            return {
                "shortlist": False,
                "score": 60,
                "reasons": [
                    "Unable to parse structured recommendation from LLM. Please review the analysis above."
                ],
                "upskill_plan": "Please refer to the improvement suggestions in the analysis.",
                "alternative_roles": ["ML Engineer", "Data Engineer"]
            }

    def initial_analysis(self) -> dict:
        """
        Run the initial ATS analysis and return both the long‑form analysis
        and a structured recommendation.
        """
        if not self.resume_context or not self.job_context:
            raise RuntimeError("Context not available. Run retrieve_chunks() first.")

        # 1. Full analysis (long text)
        analysis_prompt = f"""
        You are an expert ATS (Applicant Tracking System) Resume Analyzer.

        **Job Description:**
        {self.job_context}

        **Candidate Resume:**
        {self.resume_context}

        Based on the above, provide a detailed analysis with the following sections:

        1. **ATS Match Percentage** – Estimate a percentage match (0-100%).
        2. **Matching Skills** – List all skills from the resume that are present in the job description.
        3. **Missing Skills** – List key skills required by the job that are missing from the resume.
        4. **Missing Keywords** – Important keywords (technologies, tools, certifications) not found in the resume.
        5. **Experience Gap** – Compare years of experience and relevant domain experience.
        6. **Strengths** – Highlight the candidate's strongest areas relative to the job.
        7. **Improvement Suggestions** – Specific actionable suggestions to improve the resume for this job.
        8. **Final Recommendation** – Should the candidate be shortlisted? Why or why not?

        Be concise but thorough.
        """
        analysis_response = self.llm.invoke(analysis_prompt)
        analysis_text = analysis_response.content

        # 2. Structured recommendation
        rec_data = self._get_recommendation()

        return {
            "analysis": analysis_text,
            "recommendation": rec_data
        }

    def ask_question(self, user_question: str) -> str:
        """Answer a follow‑up question based on the stored contexts."""
        if not self.resume_context or not self.job_context:
            raise RuntimeError("Context not available. Run retrieve_chunks() first.")

        follow_up_prompt = f"""
        You are an ATS expert. Use the following Job Description and Resume context to answer the user's question.
        Answer **only** based on the provided context. If the context does not contain the answer, say "I don't have enough information to answer that."

        **Job Description:**
        {self.job_context}

        **Candidate Resume:**
        {self.resume_context}

        **User Question:**
        {user_question}

        **Answer:**
        """
        response = self.llm.invoke(follow_up_prompt)
        return response.content