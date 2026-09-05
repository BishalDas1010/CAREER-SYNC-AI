import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# FastAPI gives us the tools needed to create our API
# File -> tells FastAPI that we are receiving a file
# UploadFile -> represents the file that the user uploads
# HTTPException -> helps us send proper error messages to the user
from fastapi import FastAPI, File, UploadFile, HTTPException

# shutil is a Python library that helps us copy/save files
import shutil

# Path makes it easier to work with folders and file paths
from pathlib import Path
#document chunking
from mainCode.docs_loader import docs_loader



# CREATE OUR FASTAPI APPLICATION
# Think of "app" as our actual backend/server.
# Everything we create later (routes/endpoints) will
# be connected to this app.
app = FastAPI(
    title="Resume Upload API",
    description="Upload your resume file"
)


# CREATE A FOLDER FOR RESUMES
# We want to store the resumes uploaded by users
# inside a folder called "uploads".
#
# Path("uploads") means:
# "Hey Python, the folder I want to work with is
#  called uploads."
upload_dir = Path("uploads")


# Create the "uploads" folder if it doesn't exist.
#
# exist_ok=True means:
# "If the folder is already there, that's completely fine.
#  Don't give me an error."
#
# So when we start the backend:
#
#   If uploads/ doesn't exist → CREATE IT
#   If uploads/ already exists → DO NOTHING
upload_dir.mkdir(exist_ok=True)


#create a upload end point
@app.post("/upload")
#async is function that runs when someone call the end point
#file:uploadFile this expact the file 
#this file is going to come from a file upload 
#(...) this mean the file if requeid or never be none
async def upload_Resume(file:UploadFile = File(...)):
    #only this extension files are allowed
    allowed_extensions = {".pdf", ".docx", ".doc", ".txt", ".rtf"}
    file_extensions = Path(file.filename).suffix.lower()
    if file_extensions not in allowed_extensions:
       raise HTTPException(
        status_code=400,
        detail=f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        )
    #we just fatch the file name here from the path 
    safe_filename = Path(file.filename).name
    #now combine with uploaded folder with the file name 
    file_path = upload_dir / safe_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file,buffer)

    except Exception as e :
        raise HTTPException(
            status_code= 500,
            detail=f"failed to save the file {str(e)}")
    finally:
        await file.close()


    try:
        #load the file
        processor = docs_loader(file_path)
        file_type = processor.get_loader_type()   # returns 'pdf', 'text', 'csv' or None
        
        # chack the file type
        if file_type not in ['pdf', 'text', 'csv']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}. Allowed types are .pdf, .txt, .csv."
            )

        # Load the documents and store 
        documents = processor.document_load(file_type)
        
        # Chunk the documents – define your own CHUNK_SIZE and CHUNK_OVERLAP
        CHUNK_SIZE = 500
        CHUNK_OVERLAP = 250
        chunks = processor.chunking(documents, CHUNK_SIZE, CHUNK_OVERLAP)
        # (Optional: do something with chunks, e.g., store in vector DB)

    except HTTPException:
        # Re-raise HTTP exceptions so they are handled by FastAPI
        raise
    except Exception as e:
        # Print the full error traceback to the console for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred while processing the file: {str(e)}"
        )

    return {

        # A simple success message
        "message": "Resume uploaded successfully",

        # The original filename
        # Example: "Vishal_Resume.pdf"
        "filename": file.filename,

        # What type of file was uploaded
        # Example: "application/pdf"
        "content_type": file.content_type,

        # How large the saved file is in bytes
        # Example: 245678 bytes
        "size_bytes": file_path.stat().st_size,

        # Where the file was saved
        # Example: "uploads/Vishal_Resume.pdf"
        "saved_path": str(file_path)
    }