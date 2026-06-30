# app.py
import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000"  # Adjust if deployed elsewhere

st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
st.title("📄 ATS Resume Analyzer")

# Sidebar for file uploads
with st.sidebar:
    st.header("Upload Documents")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])
    
    if st.button("Upload and Index", type="primary"):
        if resume_file and job_file:
            # Upload resume
            files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
            r1 = requests.post(f"{API_BASE}/upload_resume", files=files)
            if r1.status_code != 200:
                st.error(f"Resume upload failed: {r1.text}")
            else:
                # Upload job description
                files = {"file": (job_file.name, job_file.getvalue(), "text/plain")}
                r2 = requests.post(f"{API_BASE}/upload_jobdesc", files=files)
                if r2.status_code != 200:
                    st.error(f"Job description upload failed: {r2.text}")
                else:
                    st.success("Both documents uploaded and indexed successfully!")
                    st.session_state["ready"] = True
        else:
            st.warning("Please upload both files.")

# Main area
if "ready" not in st.session_state:
    st.session_state["ready"] = False

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Run Initial Analysis", disabled=not st.session_state["ready"]):
        with st.spinner("Analyzing..."):
            resp = requests.post(f"{API_BASE}/analyze")
            if resp.status_code == 200:
                analysis = resp.json()["analysis"]
                st.session_state["analysis"] = analysis
            else:
                st.error(f"Analysis failed: {resp.text}")

with col2:
    if "analysis" in st.session_state:
        st.markdown(st.session_state["analysis"])

# Q&A section
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