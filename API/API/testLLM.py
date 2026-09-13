from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY_GROQ")
if not GROQ_API_KEY:
    raise ValueError("Groq API key not found in environment variables (GROQ_KEY).")


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0
)

response = llm.invoke("Analyze this resume and list the top skills.")

print(response.content)