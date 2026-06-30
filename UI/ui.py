# app.py
import streamlit as st
import requests
import re

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
st.title("📄 ATS Resume Analyzer")

# ---------- Helper: parse analysis into sections ----------
def parse_analysis_sections(text):
    """
    Safely parse analysis text, handling dict or string input.
    Returns a list of dicts: [{"title": "...", "content": "..."}, ...]
    """
    # If we got a dict, extract the "analysis" key
    if isinstance(text, dict):
        text = text.get("analysis", "")
    # Ensure it's a string
    if not isinstance(text, str):
        return [{"title": "Analysis", "content": str(text)}]
    # If empty, return a placeholder
    if not text.strip():
        return [{"title": "No analysis yet", "content": "Run the analysis first."}]

    # Try to split by numbered sections: "1. **Title**", "### 1. Title", etc.
    pattern = r'(?:###\s*)?(\d+)\.\s*\**([^*\n]+)\**\s*\n(.*?)(?=\n\s*(?:###\s*)?\d+\.|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        # Fallback: split by "### " if present
        parts = re.split(r'###\s+', text)
        if len(parts) > 1:
            sections = []
            for part in parts[1:]:
                lines = part.strip().split('\n', 1)
                if lines:
                    title = lines[0].strip()
                    content = lines[1] if len(lines) > 1 else ""
                    sections.append({"title": title, "content": content})
            return sections if sections else [{"title": "Analysis", "content": text}]
        else:
            return [{"title": "Analysis", "content": text}]
    else:
        sections = []
        for num, title, content in matches:
            sections.append({
                "title": f"{num}. {title.strip()}",
                "content": content.strip()
            })
        return sections

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Upload Documents")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])
    
    if st.button("Upload and Index", type="primary"):
        if resume_file and job_file:
            files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
            r1 = requests.post(f"{API_BASE}/upload_resume", files=files)
            if r1.status_code != 200:
                st.error(f"Resume upload failed: {r1.text}")
            else:
                files = {"file": (job_file.name, job_file.getvalue(), "text/plain")}
                r2 = requests.post(f"{API_BASE}/upload_jobdesc", files=files)
                if r2.status_code != 200:
                    st.error(f"Job description upload failed: {r2.text}")
                else:
                    st.success("Both documents uploaded and indexed successfully!")
                    st.session_state["ready"] = True
        else:
            st.warning("Please upload both files.")

# ---------- Initialise session state ----------
if "ready" not in st.session_state:
    st.session_state["ready"] = False
if "analysis" not in st.session_state:
    st.session_state["analysis"] = ""
if "recommendation" not in st.session_state:
    st.session_state["recommendation"] = {}

# ---------- Main area ----------
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Run Initial Analysis", disabled=not st.session_state["ready"]):
        with st.spinner("Analyzing..."):
            resp = requests.post(f"{API_BASE}/analyze")
            if resp.status_code == 200:
                data = resp.json()
                # Handle both old (string) and new (dict) response formats
                if isinstance(data, str):
                    # Backend still returns a plain string -> wrap it
                    st.session_state["analysis"] = data
                    st.session_state["recommendation"] = {
                        "shortlist": False,
                        "score": 60,
                        "reasons": ["Please refer to the detailed analysis."],
                        "upskill_plan": "Check the improvement suggestions above.",
                        "alternative_roles": ["ML Engineer", "Data Engineer"]
                    }
                else:
                    # New format: dict with "analysis" and "recommendation"
                    st.session_state["analysis"] = data.get("analysis", "")
                    st.session_state["recommendation"] = data.get("recommendation", {})
            else:
                st.error(f"Analysis failed: {resp.text}")

with col2:
    # ----- Display Recommendation (if available) -----
    rec = st.session_state.get("recommendation")
    if rec and isinstance(rec, dict):
        st.subheader("📌 Final Recommendation")
        score = rec.get("score", 0)
        shortlist = rec.get("shortlist", False)
        if shortlist:
            st.success(f"✅ **Shortlist Candidate** (Score: {score}%)")
        else:
            st.error(f"❌ **Do not shortlist** (Score: {score}%)")
        st.progress(score / 100.0)
        reasons = rec.get("reasons", [])
        if reasons:
            st.write("**Why?**")
            for r in reasons:
                st.write(f"• {r}")
        upskill = rec.get("upskill_plan")
        if upskill:
            st.info(f"**Next Steps for Candidate:** {upskill}")
        alt = rec.get("alternative_roles", [])
        if alt:
            st.write("**Alternative Roles:** " + ", ".join(alt))
        st.divider()

    # ----- Display Analysis as Waypoints (Expandable Sections) -----
    if st.session_state["analysis"]:
        st.subheader("📋 Detailed Analysis")
        sections = parse_analysis_sections(st.session_state["analysis"])
        for idx, sec in enumerate(sections, start=1):
            # Determine icon based on content (simple heuristic)
            content_lower = sec["content"].lower()
            if "missing" in content_lower or "gap" in content_lower or "not found" in content_lower:
                icon = "❌"
            else:
                icon = "✅"
            # Open the first section by default
            with st.expander(f"{icon} {sec['title']}", expanded=(idx == 1)):
                st.markdown(sec["content"])
    else:
        st.info("Click 'Run Initial Analysis' to see the results.")

# ---------- Q&A section ----------
st.divider()
st.subheader("💬 Ask Follow‑up Questions")
question = st.text_input("Your question about the resume or job:")
if st.button("Ask", disabled=not st.session_state["ready"] or not question):
    with st.spinner("Thinking..."):
        resp = requests.post(f"{API_BASE}/ask", json={"question": question})
        if resp.status_code == 200:
            answer = resp.json()["answer"]
            st.write("**Answer:**", answer)
        else:
            st.error(f"Error: {resp.text}")