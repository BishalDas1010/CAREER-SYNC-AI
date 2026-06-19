from langchain_community.document_loaders import PyPDFLoader   # correct loader for PDFs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings   # LangChain-compatible wrapper

def pdf_loader(pdf_path):
    """Load a PDF and return the list of documents."""
    loader = PyPDFLoader(pdf_path)   # use the correct loader
    return loader.load()             # no argument, returns list of Documents

def Text_spliter(docs, splitter):
    """Split documents and optionally print chunks."""
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}")
        print(chunk.page_content)
        print("-" * 30)
    return chunks

def Embedding_gena(model, chunks):
    return model   

def vactor_store(chunks, embedding_model):
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,           # pass the model, not precomputed vectors
        persist_directory="./chroma_db"
    )
    return vectorstore

def retriver(query, vectorstore):
    """Query the vector store and print results."""

    results = vectorstore.similarity_search(query, k=3)
    for res in results:
        print(res.page_content)
    return results


# Load PDF
docs = pdf_loader("3242969.3242985.pdf")   # make sure file exists

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
chunks = Text_spliter(docs, splitter)

# Create embedding model (use HuggingFaceEmbeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embeddings = Embedding_gena(embedding_model, chunks)   # returns embedding_model

#  Create vector store
vectorstore = vactor_store(chunks, embeddings)   # embeddings is the model

#  Query
retriver("what is this paper ?", vectorstore)