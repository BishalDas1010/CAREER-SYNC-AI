import os
from dotenv import load_dotenv
from textLoader.ResumeLoader import ResumeLoader
from textLoader.docs_loader import docs_loader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI

load_dotenv()

class API:
    def __init__(self):
        # Configuration – these can be overridden when needed
        self.RESUME_PATH = "Bishaldas_cv_.pdf"
        self.JOB_DESC_PATH = "job_des.txt"
        self.EMBEDDING_MODEL = "all-MiniLM-L6-v2"
        self.CHUNK_SIZE = 500
        self.CHUNK_OVERLAP = 100
        self.RETRIEVER_K = 5
        self.MMR_LAMBDA_RESUME = 0.9
        self.MMR_LAMBDA_JOB = 0.8

        # These will be set during execution
        self.embedding_model = None
        self.resume_vectorstore = None
        self.job_vectorstore = None
        self.resume_context = None
        self.job_context = None
        self.llm = None

    #  FIXED: embedding model loading 
    def Embedding_Model(self):
        """Load HuggingFace embeddings, fallback to CPU if CUDA fails."""
        try:
            embedding_model = HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL,
                model_kwargs={'device': 'cuda'}
            )
            # Test the model
            _ = embedding_model.embed_query("test")
            print("Embedding model loaded on GPU.")
            return embedding_model
        except Exception:
            print("CUDA not available, falling back to CPU.")
            embedding_model = HuggingFaceEmbeddings(
                model_name=self.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
            return embedding_model   # <-- FIX: return the CPU model

    # FIXED: text splitter creation 
    def text_splitter(self):
        """Return a RecursiveCharacterTextSplitter instance."""
        return RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.CHUNK_OVERLAP
        )

    # load and index resume 
    def load_resume(self):
        """Load resume PDF, split, and build vector store."""
        try:
            splitter = self.text_splitter()
            loader = ResumeLoader(self.RESUME_PATH, self.embedding_model)
            docs = loader.pdf_loader()
            chunks = loader.text_splitter(docs, splitter)
            vectorstore = loader.vector_store(chunks, self.embedding_model)
            print("Resume loaded and indexed.")
            return vectorstore
        except Exception as e:
            raise RuntimeError(f"Error processing resume: {e}")

    #  load and index job description -------------------
    def load_job_description(self):
        """Load job description (assumes .txt file), split, and build vector store."""
        try:
            splitter = self.text_splitter()
            loader = docs_loader(self.JOB_DESC_PATH, self.embedding_model)
            docs = loader.pdf_loader()   # Note: works if docs_loader handles .txt too
            chunks = loader.text_splitter(docs, splitter)
            vectorstore = loader.vector_store(chunks, self.embedding_model)
            print("Job description loaded and indexed.")
            return vectorstore
        except Exception as e:
            raise RuntimeError(f"Error processing job description: {e}")

    #retrieve relevant chunks -------------------
    def retrieve_chunks(self):
        """Use MMR to get most relevant chunks from both documents."""
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

        # Store contexts as instance variables for later use
        self.resume_context = "\n\n".join([doc.page_content for doc in retrieved_resume])
        self.job_context = "\n\n".join([doc.page_content for doc in retrieved_job])

        print("Relevant chunks retrieved successfully.")

    # LLM initialization -------------------
    def LLM_Load(self):
        """Initialize the Mistral LLM."""
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.3
        )
        return self.llm

    # FIXED: initial analysis -------------------
    def initial_analysis(self):
        """Perform the first ATS analysis and print results."""
        if not self.resume_context or not self.job_context:
            raise RuntimeError("Context not available. Run retrieve_chunks() first.")

        initial_prompt = f"""
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

        try:
            print("\n" + "="*60)
            print("Initial ATS Analysis (this may take a moment)...")
            print("="*60)
            response = self.llm.invoke(initial_prompt)
            print(response.content)
            print("\n" + "="*60)
        except Exception as e:
            raise RuntimeError(f"Error during initial analysis: {e}")

    # FIXED: interactive Q&A loop 
    def qAndANS(self):
        """Interactive follow-up question loop using stored contexts."""
        if not self.resume_context or not self.job_context:
            raise RuntimeError("Context not available. Run retrieve_chunks() first.")

        print("\nYou can now ask follow‑up questions about the resume and job.")
        print("Type 'exit' or 'quit' to end the conversation.\n")

        while True:
            user_question = input("Your question: ").strip()
            if user_question.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break
            if not user_question:
                continue

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
            try:
                response = self.llm.invoke(follow_up_prompt)
                print("\nAnswer:", response.content, "\n")
            except Exception as e:
                print(f"Error: {e}")

    # NEW: main orchestration method 
    def run(self):
        """Run the entire ATS analysis pipeline."""
        print("="*60)
        print("Starting ATS Resume Analyzer")
        print("="*60)

        # Step 1: Load embedding model
        self.embedding_model = self.Embedding_Model()

        # Step 2: Load and index documents
        self.resume_vectorstore = self.load_resume()
        self.job_vectorstore = self.load_job_description()

        # Step 3: Retrieve relevant chunks
        self.retrieve_chunks()

        # Step 4: Initialize LLM
        self.LLM_Load()

        # Step 5: Initial analysis
        self.initial_analysis()

        # Step 6: Interactive Q&A
        self.qAndANS()


#  Usage 
if __name__ == "__main__":
    analyzer = API()
    analyzer.run()