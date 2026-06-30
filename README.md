# CAREER-SYNC-AI

## Problem Solved
Career-Sync-AI solves the problem of evaluating a candidate resume against a job description quickly and intelligently.

Many job seekers struggle to understand whether their resume matches a job posting and which skills, keywords, or experience are missing. This project provides an ATS-style resume analysis that:

- compares a resume PDF with a job description text file
- identifies matching skills and missing skills
- estimates an ATS match score
- provides improvement suggestions and a shortlist recommendation
- answers follow-up questions about the resume and job fit

## How It Works

1. Upload the resume and job description.
2. The app converts both documents into text and splits them into chunks.
3. These chunks are embedded and stored in a vector database.
4. A retriever selects the most relevant resume and job content.
5. A language model analyzes the matched content and returns:
   - detailed ATS-style analysis
   - match percentage
   - strengths and gaps
   - improvement actions
   - a final recommendation

## Key Components

- `UI/ui.py` - Streamlit front-end for uploading documents, running analysis, and asking questions.
- `mainCode/ats_analyzer.py` - Core analysis service that builds embeddings, retrieves relevant context, and calls the LLM.
- `mainCode/main.py` - Example CLI flow for loading documents, indexing them, and running analysis.
- `mainCode/textLoader/ResumeLoader.py` and `mainCode/textLoader/docs_loader.py` - document loaders and vector store builders.

## Why This Matters

This project helps job seekers and hiring teams by turning resume and job description comparison into an automated, explainable process. It removes manual guesswork and highlights where the candidate is a strong fit or where the resume needs improvement.

## Usage

- Upload a resume in PDF format.
- Upload a job description in TXT format.
- Run the analysis to see a detailed report and recommendation.
- Ask follow-up questions to explore specific resume or job details.

## Notes

- The system uses embeddings and an LLM to understand semantic similarity.
- It is designed to work like an ATS-aware resume reviewer, not just a keyword matcher.
- The project currently expects local model/LLM access through configured environment settings.