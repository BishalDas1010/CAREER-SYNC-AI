import sys
import os
import shutil
import logging
from pathlib import Path
from pydantic import BaseModel,Field
from langchain_groq import ChatGroq
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.embeddings import HuggingFaceEmbeddings
# Document chunking
from mainCode.docs_loader import docs_loader
from llm_analysis import analyze_resume
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Allow pyhton to find filles /modules from the project 
#__file__ = the location of current pyhton file 
#.parent .parent  =go one more folder up(project root)
#sys(...)= cpnver the path into str
#sys.path.append (...)= tell py also search this folder
sys.path.append(str(Path(__file__).parent.parent))


# Logging 
#instand of using print() everywhere we use a logger 
#"resume_api" is simply the name we gave to the logger 
#this heps us odentify which part of the project genrate the particular message 

logger = logging.getLogger("resume_api")


#“Set up Python's logging system, and show me messages that are INFO level or more important.”
logging.basicConfig(level=logging.INFO)


# Config 

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv"}
MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB
CHUNK_SIZE = 500
CHUNK_OVERLAP = 250

UPLOAD_DIR = Path(__file__).parent / "uploads"
#if the file exist then continue if not then create
UPLOAD_DIR.mkdir(exist_ok=True)


#  App 

app = FastAPI(
    title="Resume Upload API",
    description="Upload your resume file",
)
# This line is basically used to decide which frontend web
# sites are allowed to communicate with your backend API.
origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#request Model 
class ChatRequest(BaseModel):
    message :str = Field(
        ...,
        min_length=1,
        max_length= 2000
    ),
    #conversation_id can contain either an integer (int) 
    # or None, and its default value is None
    conversarion_id : int | None = None 
    resume_id :int |None = None


#  Routes

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # 1. Validate extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # 2. Validate size (read once into memory)
    contents = await file.read()
    if len(contents) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size is {MAX_FILE_BYTES // (1024 * 1024)} MB.",
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    # 3. Save file
    try:
        file_path.write_bytes(contents)
    except Exception as e:
        logger.exception("Failed to save uploaded file")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save the file: {str(e)}",
        )
    finally:
        await file.close()

    # 4. Load -> chunk -> analyze (all in the same request)
    try:
        processor = docs_loader(file_path)
        file_type = processor.get_loader_type()  # 'pdf' | 'text' | 'csv' | None
        logger.info("Detected loader type: %s", file_type)

        if file_type not in ("pdf", "text", "csv"):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}. Allowed types are .pdf, .txt, and .csv.",
            )

        documents = processor.document_load(file_type)
        chunks = processor.chunking(documents, CHUNK_SIZE, CHUNK_OVERLAP)
        analysis = analyze_resume(chunks, file_type)

    except HTTPException:
        raise
    except ValueError as e:
        # e.g."No extractable text found in the uploaded file."
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.exception("Internal error while processing the file")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred while processing the file: {str(e)}",
        )

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": file_path.stat().st_size,
        "saved_path": str(file_path),
        "analysis": analysis,
    }



@app.post("/chatWithAi")
async def chat(Chat_request:ChatRequest):
    message  =Chat_request.message
    conversation_id = Chat_request.conversarion_id
    resume_id = Chat_request.resume_id
    #message chunking and embadding conversion
    try:
        Embadding = HuggingFaceEmbeddings(
            model_name = "all-MiniLM-L6-v2",
            model_kwargs ={"device":"cuda"}

        )
        _ = Embadding.embed_query("test")

    except Exception:
        print("cuda is not available, falling back to cpu")

        Embadding = HuggingFaceEmbeddings(
            model_name = "all-MiniLM-L6-v2",
            model_kwargs ={"device":"cpu"}

        )
    message_query = Embadding.embed_query(message)
    searching = docs_loader()
    vactorstore =searching.vector_store()
    result = vactorstore.similarity_search(
        message_query,
        k=5
    )
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
    You are Career Sync AI.

    Answer the user's question based only on the provided context.

    If the context does not contain enough information to answer,
    say that you don't have enough information.

    Context:
    {context}

    User question:
    {question}

    Answer:
    """)
    ai_response = llm.invoke(prompt)

    
    return{
        "message":message,
        "conversation_id":conversation_id,
        "resume_id":resume_id,
        "Ai_responce":ai_response
    }