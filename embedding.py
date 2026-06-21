from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("3242969.3242985.pdf")
docs = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(docs)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Extract text from chunks
texts = [chunk.page_content for chunk in chunks]

# Generate embeddings
embeddings = model.encode(texts)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)