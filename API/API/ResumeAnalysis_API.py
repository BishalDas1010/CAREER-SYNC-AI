import sys
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
from pathlib import Path

# document chunking
from mainCode.docs_loader import docs_loader

from llm_analysis import analyze_resume
# analysis logic now lives in its own module - imported, not redefined inline

app = FastAPI(
    title="Resume Upload API",
    description="Upload your resume file"
)

# Allowed origins - set via environment variable or list
# Default covers both CRA (3000) and Vite (5173) dev servers
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)


@app.post("/upload")
async def upload_Resume(file: UploadFile = File(...)):
    # only these extensions are allowed
    allowed_extensions = {".pdf", ".docx", ".doc", ".txt", ".rtf"}
    file_extensions = Path(file.filename).suffix.lower()
    if file_extensions not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        )

    safe_filename = Path(file.filename).name
    file_path = upload_dir / safe_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"failed to save the file {str(e)}"
        )
    finally:
        await file.close()

    # --- Everything below runs automatically, in the same request, ---
    # --- right after the file is saved: load -> chunk -> analyze.   ---
    try:
        processor = docs_loader(file_path)
        file_type = processor.get_loader_type()  # returns 'pdf', 'text', 'csv' or None
        print(file_type)
        if file_type not in ['pdf', 'text', 'csv']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}. Allowed types are .pdf, .txt, .csv."
            )

        documents = processor.document_load(file_type)

        CHUNK_SIZE = 500
        CHUNK_OVERLAP = 250
        chunks = processor.chunking(documents, CHUNK_SIZE, CHUNK_OVERLAP)

        # analysis runs automatically here - no separate endpoint/call needed
        analysis = analyze_resume(chunks, file_type)

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred while processing the file: {str(e)}"
        )

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": file_path.stat().st_size,
        "saved_path": str(file_path),
        "analysis": analysis,
    }