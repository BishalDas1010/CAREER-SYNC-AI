from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
    )

from langchain_text_splitters import RecursiveCharacterTextSplitter


class docs_loader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # Step 1: Document type detection
    def get_loader_type(self):

        extension = Path(self.pdf_path).suffix.lower()

        loaders = {
            ".pdf": "pdf",
            ".txt": "text",
            ".csv": "csv"

        }

        return loaders.get(extension, None)

    # PDF loader
    def pdf_loader(self):
        loader = PyPDFLoader(self.pdf_path)
        return loader.load()

    def text_loader(self):
        # Add encoding fallback to avoid UnicodeDecodeError
        loader = TextLoader(self.pdf_path, encoding='utf-8')
        try:
            return loader.load()
        except UnicodeDecodeError:
            # Fallback to a different encoding if utf-8 fails
            loader = TextLoader(self.pdf_path, encoding='latin-1')
            return loader.load()

    def csv_loader(self):
        loader = CSVLoader(self.pdf_path)
        return loader.load()
    

    def document_load(self, typee):

        if typee == "pdf":
            return self.pdf_loader()

        elif typee == "text":
            return self.text_loader()

        elif typee == "csv":
            return self.csv_loader()

        else:
            raise ValueError(f"Unsupported document type: {typee}")

    # Step 2: Chunking / Splitting
    def chunking(self, docs, CHUNK_SIZE, CHUNK_OVERLAP):
        # If no documents were loaded, return empty list
        if not docs:
            return []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        chunks = text_splitter.split_documents(docs)
        return chunks