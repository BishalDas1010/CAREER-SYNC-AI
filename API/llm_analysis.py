from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Literal
from dotenv import load_dotenv
import os
import json
from pathlib import Path


GROQ_API_KEY = ""


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add GROQ_API_KEY or API_KEY_GROQ to API/.env"
    )


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


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0,
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert resume and ATS analyzer.

Analyze the resume carefully.

Return ONLY valid JSON.

The JSON must follow this structure:

{{
  "scoreCards": [
    {{
      "label": "string",
      "value": 0,
      "suffix": "string",
      "status": "good",
      "tone": "positive"
    }}
  ],
  "sections": [
    {{
      "name": "string",
      "score": 0,
      "status": "good"
    }}
  ],
  "matchedKeywords": [],
  "missingKeywords": [],
  "suggestions": [
    {{
      "priority": "high",
      "title": "string",
      "detail": "string"
    }}
  ]
}}

Rules:

- Scores must be between 0 and 100.
- status must be one of: good, warning, bad.
- tone must be one of: positive, neutral, negative.
- priority must be one of: high, medium, low.
- Do not invent information that isn't present in the resume.
- Return ONLY JSON.
"""
    ),
    (
        "human",
        """
Resume:

{resume}
"""
    )
])


chain = prompt | llm


def analyze_resume(chunks, file_type):

    resume_text = "\n\n".join(
        chunk.page_content for chunk in chunks
    ).strip()

    if not resume_text:
        raise ValueError(
            "No extractable text found in the uploaded file."
        )

    response = chain.invoke({
        "resume": resume_text
    })

    content = response.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Groq returned invalid JSON: {e}\nResponse: {content}"
        )

    result = ResumeAnalysis.model_validate(data)

    return result.model_dump()