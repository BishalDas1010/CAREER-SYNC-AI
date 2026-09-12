from docs_loader import pdf_upload
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
import os
API_key  = os. getenv("API_KEY")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
pdf_path = "/home/vishal/Career-Sync-AI/mainCode/Bishaldas.pdf"

#obj of pdf_upload
pdf_loaderr = pdf_upload(pdf_path=pdf_path)
type_of_doco = pdf_loaderr.get_loader_type()
docs = pdf_loaderr.document_load(type_of_doco)
chunks = pdf_loaderr.chunking(docs=docs,CHUNK_SIZE=500,CHUNK_OVERLAP=100)

for i,content in enumerate(chunks):
    print(f"chunks,{i}")
    print(content.page_content)

embadding = HuggingFaceEmbeddings(
        model_name= EMBEDDING_MODEL,
        model_kwargs={'device': 'cuda'}
)

vactor_store =Chroma.from_documents(
    documents = chunks,
    embedding= embadding,
    persist_directory="./chroma_db"
)



print("save successfully!")
