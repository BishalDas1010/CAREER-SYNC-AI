
from docs_loader import pdf_upload

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_mistralai import ChatMistralAI

import os
from dotenv import load_dotenv


#=======================================================
# 1. LOAD ENVIRONMENT VARIABLES
#=======================================================

load_dotenv()

API_key = os.getenv("API_KEY")

llm = ChatMistralAI(model="mistral-large-latest", temperature=0.3)
ans =llm.invoke("what is my name")
print(ans)