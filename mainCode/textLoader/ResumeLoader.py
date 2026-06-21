from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class ResumeLoader:

    def __init__(self, pdf_path, model):
        self.pdf_path = pdf_path
        self.model = model

    def pdf_loader(self):
        loader = PyPDFLoader(self.pdf_path)
        return loader.load()

    def text_splitter(self, docs, splitter):
        chunks = splitter.split_documents(docs)

        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}")
            print(chunk.page_content)
            print("-" * 30)

        return chunks

    def embedding_gen(self):
        return HuggingFaceEmbeddings(
            model_name=self.model
        )

    def vector_store(self, chunks, embedding_model):
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="./chroma_db"
        )
        return vectorstore

    def retriever(self, query, vectorstore):
        results = vectorstore.similarity_search(query, k=3)

        for res in results:
            print(res.page_content)

        return results