import os
from dotenv import load_dotenv
from textLoader.ResumeLoader import ResumeLoader
from textLoader.docs_loader import docs_loader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI

# Load environment (API key)
load_dotenv()

def main():
    # Configuration 
    RESUME_PATH = "Bishaldas_cv_.pdf"
    JOB_DESC_PATH = "job_des.txt"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    RETRIEVER_K = 5
    MMR_LAMBDA_RESUME = 0.9
    MMR_LAMBDA_JOB = 0.8

    #  Embedding Model
    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cuda'}
        )

        #it just chack the model load correctly or not
        _ = embedding_model.embed_query("test")
    except Exception:
        print("CUDA not available, falling back to CPU.")
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    #Load Resume 
    try:
        resume_loader = ResumeLoader(RESUME_PATH, embedding_model)
        resume_docs = resume_loader.pdf_loader()
        resume_chunks = resume_loader.text_splitter(resume_docs, text_splitter)
        resume_vectorstore = resume_loader.vector_store(resume_chunks, embedding_model)
        print("Resume loaded and indexed.")
    except Exception as e:
        print(f"Error processing resume: {e}")
        return

    # Load Job Description
    try:
        job_loader = docs_loader(JOB_DESC_PATH, embedding_model)
        job_docs = job_loader.pdf_loader()
        job_chunks = job_loader.text_splitter(job_docs, text_splitter)
        job_vectorstore = job_loader.vector_store(job_chunks, embedding_model)
        print("Job description loaded and indexed.\n")
    except Exception as e:
        print(f"Error processing job description: {e}")
        return

    # Retrieve Relevant Chunks 
    resume_query = """
    Extract the candidate's skills, technical expertise,
    projects, work experience, education,
    certifications, achievements, and relevant keywords.
    """
    job_query = """
    What skills, qualifications, experience, responsibilities,
    and technologies are required for this job?
    """

    resume_retriever = resume_vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": RETRIEVER_K, "lambda_mult": MMR_LAMBDA_RESUME}
    )
    job_retriever = job_vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": RETRIEVER_K, "lambda_mult": MMR_LAMBDA_JOB}
    )

    retrieved_resume = resume_retriever.invoke(resume_query)
    retrieved_job = job_retriever.invoke(job_query)

    if not retrieved_resume or not retrieved_job:
        print("No relevant chunks retrieved. Check document content.")
        return

    resume_context = "\n\n".join([doc.page_content for doc in retrieved_resume])
    job_context = "\n\n".join([doc.page_content for doc in retrieved_job])

    #  Build Initial Analysis Prompt
    initial_prompt = f"""
    You are an expert ATS (Applicant Tracking System) Resume Analyzer.

    **Job Description:**
    {job_context}

    **Candidate Resume:**
    {resume_context}

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

    #  LLM Initialisation 
    llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0.3
    )

    # Initial Analysis 
    try:
        print("\n" + "="*60)
        print("Initial ATS Analysis (this may take a moment)...")
        print("="*60)
        response = llm.invoke(initial_prompt)
        print(response.content)
        print("\n" + "="*60)
    except Exception as e:
        print(f" Error during initial analysis: {e}")
        return

    # -Interactive Q&A Loop 
    print("\n You can now ask follow‑up questions about the resume and job.")
    print("   Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_question = input(" Your question: ").strip()
        if user_question.lower() in ["exit", "quit", "bye"]:
            print(" Goodbye!")
            break
        if not user_question:
            continue

        # Build a prompt that uses the same context and answers the specific question
        follow_up_prompt = f"""
    You are an ATS expert. Use the following Job Description and Resume context to answer the user's question.
    Answer **only** based on the provided context. If the context does not contain the answer, say "I don't have enough information to answer that."

    **Job Description:**
    {job_context}

    **Candidate Resume:**
    {resume_context}

    **User Question:**
    {user_question}

    **Answer:**
    """
        try:
            response = llm.invoke(follow_up_prompt)
            print("\n Answer:", response.content, "\n")
        except Exception as e:
            print(f" Error: {e}")

if __name__ == "__main__":
    main()