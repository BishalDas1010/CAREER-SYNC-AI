from langchain_chroma import Chroma
import os
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
load_dotenv()
mistral_api_key = os.getenv("LLM_MISTRAL_API_KEY")
if not mistral_api_key:
    raise ValueError("Mistral API key not found ")

def analyze_resume(chunks, file_type):
    """
    Given a list of text chunks, return analysis data matching the UI structure.
    This is a placeholder - you can later integrate with an LLM or rule-based system.
    """
    # Dummy data - in reality you'd parse sections, extract keywords, etc.
    score_cards = [
        {"label": "Overall Score", "value": 10, "suffix": "/100", "status": "Good", "tone": "good"},
        {"label": "ATS Compatibility", "value": 92, "suffix": "%", "status": "Excellent", "tone": "good"},
        {"label": "Keywords Matched", "value": 24, "suffix": "/35", "status": "Improve", "tone": "warn"},
        {"label": "Readability", "value": "A-", "suffix": "", "status": "Strong", "tone": "good"},
    ]
    sections = [
        {"name": "Contact Information", "score": 100, "status": "complete"},
        {"name": "Professional Summary", "score": 85, "status": "complete"},
        {"name": "Work Experience", "score": 74, "status": "complete"},
        {"name": "Skills", "score": 60, "status": "warn"},
        {"name": "Education", "score": 100, "status": "complete"},
        {"name": "Projects", "score": 45, "status": "missing"},
    ]
    matched = ["Python", "REST APIs", "Git", "SQL", "Data Structures", "FastAPI", "Docker"]
    missing = ["Kubernetes", "LangChain", "System Design", "CI/CD", "AWS"]
    suggestions = [
        {
            "priority": "High",
            "title": "Add measurable impact to your project bullets",
            "detail": "3 of 5 project descriptions lack quantified outcomes."
        },
        # ... more suggestions
    ]
    return {
        "scoreCards": score_cards,
        "sections": sections,
        "matchedKeywords": matched,
        "missingKeywords": missing,
        "suggestions": suggestions,
    }
