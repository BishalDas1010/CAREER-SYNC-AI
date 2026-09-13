from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Literal
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("API_KEY_GROQ")
if not GROQ_API_KEY:
    raise ValueError("Groq API key not found in environment variables (GROQ_KEY).")


# Schemas 

class ScoreCard(BaseModel):
    label: str
    value: int | str
    suffix: str
    status: Literal["good", "warning", "bad"]
    tone: Literal["positive", "neutral", "negative"]


class Section(BaseModel):
    name: str
    score: int
    status: Literal["good", "warning", "bad"]


class Suggestion(BaseModel):
    priority: Literal["high", "medium", "low"]
    title: str
    detail: str


class ResumeAnalysis(BaseModel):
    scoreCards: List[ScoreCard]
    sections: List[Section]
    matchedKeywords: List[str]
    missingKeywords: List[str]
    suggestions: List[Suggestion]


#  LLM 

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0,
    max_tokens=8192,
)

structured_llm = llm.with_structured_output(ResumeAnalysis)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert resume and ATS analyzer.

        Analyze the resume carefully.

        Return:
        - Overall Score
        - ATS Compatibility
        - Keywords Matched
        - Readability
        - Section scores
        - Matched keywords
        - Missing keywords
        - Improvement suggestions

        Scores must be between 0 and 100.

        Do not invent information that isn't present
        in the resume.

        For every `status` field use only: "good", "warning", or "bad".
        For every `tone` field use only: "positive", "neutral", or "negative".
        For every suggestion `priority` use only: "high", "medium", or "low".
        """,
    ),
    (
        "human",
        """
        Resume:

        {resume}
        """,
    ),
])

chain = prompt | structured_llm


#  Entry point

def analyze_resume(chunks, file_type):

    resume_text = "\n\n".join(
        chunk.page_content for chunk in chunks
    ).strip()

    if not resume_text:
        raise ValueError("No extractable text found in the uploaded file.")

    result = chain.invoke({"resume": resume_text})
    return result.model_dump()