import os
import json
import re
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_mistralai import ChatMistralAI

# 
# Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
#predefine chunks
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
#path of the pdf
PDF_PATH = "/home/vishal/Career-Sync-AI/mainCode/Bishaldas.pdf"

#api key fatch from the .env
mistral_api_key = os.getenv("MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("Mistral API key not found in environment variables.")


# Load PDF and split into chunks
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()
print(f"PDF loaded successfully! Number of documents: {len(docs)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    add_start_index=True, #
)

chunks = text_splitter.split_documents(docs)
print(f"Total chunks: {len(chunks)}")


# Add unique chunk IDs
for i, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = f"chunk_{i}"

# Leave two blank lines before printing the next text.
print("\n\nALL CHUNKS (preview)")
for chunk in chunks:
    print("\n" + "=" * 70) # this print a single spape and === 70 timesw
    print("CHUNK ID:", chunk.metadata["chunk_id"])
    print("-" * 70)
    print(chunk.page_content[:300])  # preview only [start:end] from 0 to 300

# 
# Embeddings Genaration if Gpu not aval then shefted to CPU
try:
    embedding = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cuda"},
    )
    _ = embedding.embed_query("test")
except Exception:
    print("CUDA not available, falling back to CPU.")
    embedding = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )

#  Create vector store
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db"
)
print("Vector store saved successfully!")


# LLM and retrievers
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.2,
    mistral_api_key=mistral_api_key,
)

#similarity search into the vactor DB
similarity_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)
# Maximum marginal Relevance  retrive into the vactor DB
mmr_retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2}
)

#multi  query Retriver 
mqr_retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    ),
    llm=llm
)

#  Query and retrieve
query = "Which skills do I have?"
#dubal space 
print(f"\n\nQUERY: {query}")

# searching inside the the vactor store
similarity_docs = similarity_retriever.invoke(query)
mmr_docs = mmr_retriever.invoke(query)
mqr_docs = mqr_retriever.invoke(query)


# Helper to generate ground truth IDs using LLM
#for evalutuion of the retriver

def generate_ground_truth_ids(question, candidate_docs):
    """
    Ask the LLM which candidate chunks are actually relevant
    to answering the question.
    """
    chunks_text = ""
    for doc in candidate_docs:
        chunk_id = doc.metadata.get("chunk_id")

        chunks_text += f"""
            CHUNK_ID: {chunk_id}
            CONTENT:
            {doc.page_content}

            """
    prompt = f"""
            You are evaluating a RAG system.

            Question:
            {question}

            Below are candidate document chunks.

            Identify ALL chunks that contain information directly useful
            for answering the question.

            Return ONLY valid JSON in this format:

            {{
                "relevant_chunk_ids": ["chunk_1", "chunk_3"]
            }}

            Do not invent chunk IDs.

            Candidate chunks:
            {chunks_text}
            """
    # using LLM just chosing the TOP chunks 
    response = llm.invoke(prompt)

    raw = response.content.strip()

    print(f"\n[DEBUG] Raw LLM response:\n{raw}\n")

    # Try to extract JSON from the response
    json_str = None
    # First, try to parse as-is
    try:
        json.loads(raw)
        json_str = raw
    except json.JSONDecodeError:
        # Look for JSON inside markdown code blocks
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # Try to find anything that looks like a JSON object
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                json_str = match.group(0)
    if json_str is None:
        raise ValueError("Could not extract JSON from LLM response.")

    try:
        result = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON after extraction: {json_str}") from e

    return set(result.get("relevant_chunk_ids", []))


# Generate ground truth from the union of retrieved docs
#    (This ensures we don't miss any relevant chunk that was actually retrieved)

# Combine all retrieved documents, deduplicate by chunk_id
all_retrieved = similarity_docs + mmr_docs + mqr_docs
seen = set()
unique_docs = []
for doc in all_retrieved:
    cid = doc.metadata.get("chunk_id")
    if cid and cid not in seen:
        seen.add(cid)
        unique_docs.append(doc)

print("\nGenerating ground truth from retrieved candidates...")
ground_truth_ids = generate_ground_truth_ids(query, unique_docs)

print(f"Ground truth relevant IDs: {ground_truth_ids}")


# Print retrieved results

def print_results(name, docs):
    print("\n\n" + "=" * 70)
    print(name)
    print("=" * 70)
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Retrieved Document {i} ---")
        print("Chunk ID:", doc.metadata.get("chunk_id"))
        print("-" * 50)
        print(doc.page_content[:500])

print_results("SIMILARITY SEARCH", similarity_docs)
print_results("MMR RETRIEVER", mmr_docs)
print_results("MULTI-QUERY RETRIEVER", mqr_docs)


#  Evaluation function

def evaluate_retriever(docs, ground_truth_ids, k=2):
    retrieved_ids = []
    for doc in docs:
        chunk_id = doc.metadata.get("chunk_id")
        if chunk_id and chunk_id not in retrieved_ids:
            retrieved_ids.append(chunk_id)
        if len(retrieved_ids) == k:
            break
    retrieved_set = set(retrieved_ids)
    relevant = retrieved_set.intersection(ground_truth_ids)
    precision = len(relevant) / len(retrieved_set) if retrieved_set else 0
    recall = len(relevant) / len(ground_truth_ids) if ground_truth_ids else 0
    return precision, recall

# Compute and display metrics

sim_prec, sim_rec = evaluate_retriever(similarity_docs, ground_truth_ids, k=2)
mmr_prec, mmr_rec = evaluate_retriever(mmr_docs, ground_truth_ids, k=2)
mqr_prec, mqr_rec = evaluate_retriever(mqr_docs, ground_truth_ids, k=2)

print("\n\n")
print("=" * 70)
print("              RETRIEVER EVALUATION")
print("=" * 70)
print(f"\nSimilarity Search Precision@2: {sim_prec:.2f} and Recall@2: {sim_rec:.2f}")
print(f"MMR Retriever Precision@2: {mmr_prec:.2f} and  Recall@2: {mmr_rec:.2f}")
print(f"Multi-Query Retriever Precision@2: {mqr_prec:.2f} and Recall@2: {mqr_rec:.2f}")

print("\n\n")
print("=" * 70)
print("              FINAL COMPARISON")
print("=" * 70)
print(f"""
Retriever              Precision@2         Recall@2
------------------------------------------------------
Similarity Search      {sim_prec:.2f}  {sim_rec:.2f}
MMR Retriever          {mmr_prec:.2f}  {mmr_rec:.2f}
Multi-Query Retriever  {mqr_prec:.2f}   {mqr_rec:.2f}
""")


# Show which IDs were retrieved

print("\n--- Retrieved IDs ---")
sim_ids = [doc.metadata.get("chunk_id") for doc in similarity_docs]
mmr_ids = [doc.metadata.get("chunk_id") for doc in mmr_docs]
mqr_ids = [doc.metadata.get("chunk_id") for doc in mqr_docs]
print(f"Similarity: {sim_ids}")
print(f"MMR:        {mmr_ids}")
print(f"MQR:        {mqr_ids}")

# select the best ritriver from there 



# Dynamically select the best retriever


def f1_score(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

sim_f1 = f1_score(sim_prec, sim_rec)
mmr_f1 = f1_score(mmr_prec, mmr_rec)
mqr_f1 = f1_score(mqr_prec, mqr_rec)

retriever_scores = {
    "similarity": {"precision": sim_prec, "recall": sim_rec, "f1": sim_f1, "docs": similarity_docs},
    "mmr":        {"precision": mmr_prec, "recall": mmr_rec, "f1": mmr_f1, "docs": mmr_docs},
    "mqr":        {"precision": mqr_prec, "recall": mqr_rec, "f1": mqr_f1, "docs": mqr_docs},
}

# Pick the retriever with the highest F1; tie-break on recall
best_name = max(
    retriever_scores,
    key=lambda name: (retriever_scores[name]["f1"], retriever_scores[name]["recall"])
)
best_docs = retriever_scores[best_name]["docs"]

print("\n\n" + "=" * 70)
print("              BEST RETRIEVER SELECTED")
print("=" * 70)
for name, scores in retriever_scores.items():
    marker = " <== BEST" if name == best_name else ""
    print(f"{name:12s} F1: {scores['f1']:.2f}  (P: {scores['precision']:.2f}, R: {scores['recall']:.2f}){marker}")

print(f"\nSelected retriever: '{best_name}'")
print(f"Docs used downstream: {[d.metadata.get('chunk_id') for d in best_docs]}")




def build_context(docs):
    context_parts = []
    for doc in docs:
        chunk_id = doc.metadata.get("chunk_id")
        context_parts.append(f"[{chunk_id}]\n{doc.page_content}")
    return "\n\n".join(context_parts)

context = build_context(best_docs)

# Interactive chat loop (uses the already-selected best retriever type)

#find the best retriver 
retriever_map = {
    "similarity": similarity_retriever,
    "mmr": mmr_retriever,
    "mqr": mqr_retriever,
}
active_retriever = retriever_map[best_name]

print(f"\nUsing '{best_name}' retriever for the chat session (F1: {retriever_scores[best_name]['f1']:.2f})")

words = ["exit", "end", "out"]

while True:
    query = input("\nAsk a question: ").strip()

    if query.lower() in words:
        print("Goodbye :)")
        break

    if not query:
        continue

    # Retrieve fresh docs for THIS question using the winning retriever
    retrieved_docs = active_retriever.invoke(query)
    context = build_context(retrieved_docs)

    rag_prompt = f"""
You are a helpful assistant answering questions based ONLY on the provided context.
If the answer is not present in the context, say you don't have enough information.

Context:
{context}

Question:
{query}

Answer clearly and concisely, citing chunk IDs (like [chunk_2]) where relevant.
"""

    print("\n\n" + "=" * 70)
    print("              FINAL ANSWER GENERATION")
    print("=" * 70)

    response = llm.invoke(rag_prompt)
    answer = response.content.strip()

    print(f"\nQuestion: {query}")
    print(f"\nAnswer:\n{answer}")