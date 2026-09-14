from langchain_groq import ChatGroq
import os

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=0
)

response = llm.invoke("Analyze this resume and list the top skills.")

print(response.content)