import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_document(path):
    """Load a PDF or TXT file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".txt"):
        loader = TextLoader(path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file type – use .pdf or .txt")
    return loader.load()

def split_documents(docs, chunk_size=500, chunk_overlap=200, verbose=False):
    """Split documents and optionally print chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    if verbose:
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}\n{chunk.page_content}\n{'-'*30}")
    return chunks

def create_vector_store(chunks, embedding_model, persist_dir="./chroma_db"):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )
    return vectorstore

def query_vector_store(query, vectorstore, k=3):

    results = vectorstore.similarity_search(query, k=k)
    for i, res in enumerate(results):
        print(f"Result {i+1}:\n{res.page_content}\n")
    return results

def query_with_scores(query, vectorstore, k=3):
    """Perform search with relevance scores."""
    results = vectorstore.similarity_search_with_score(query, k=k)
    for doc, score in results:
        print(f"Score: {score}\n{doc.page_content}\n{'-'*30}")
    return results

#  Main execution 
if __name__ == "__main__":
    # 1. Load document
    file_path = "3242969.3242985.pdf"  # make sure this file exists
    docs = load_document(file_path)

    # 2. Split into chunks (verbose=False to avoid clutter)
    chunks = split_documents(docs, verbose=False)

    # 3. Create embedding model (optionally with GPU)
    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'}  # change to 'cuda' if available
    )

    # 4. Build vector store (persistent)
    vectorstore = create_vector_store(chunks, embedding_model)

    # 5. Example queries
    print("Simple Search")
    query_vector_store("what is this paper about?", vectorstore, k=3)

    print("\n Search with Scores")
    query_with_scores("What is Machine Learning?", vectorstore, k=3)