import streamlit as st

st.set_page_config(
    page_title="ResumeAI",
    page_icon="",
    layout="wide"
)

st.title(" ResumeAI ATS Analyzer")
st.caption("AI Powered Resume Screening System")

col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

with col2:
    job = st.text_area(
        "Paste Job Description",
        height=250
    )

st.divider()

if st.button("Analyze Resume", use_container_width=True):
    st.success("Resume uploaded successfully!")

st.divider()

score_col, skill_col = st.columns([1,2])

with score_col:
    st.metric("ATS Score", "84%")

with skill_col:
    st.progress(0.84)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Matching Skills")

    st.success("Python")
    st.success("FastAPI")
    st.success("SQL")
    st.success("Git")

with col2:
    st.subheader(" Missing Skills")

    st.error("Docker")
    st.error("AWS")
    st.error("Kubernetes")
    st.error("Jenkins")

st.divider()

st.subheader("Improvement Suggestions")

st.info("""
• Add Docker experience

• Mention CI/CD tools

• Improve project descriptions

• Include quantified achievements
""")

st.divider()

st.subheader("Chat with AI")

question = st.text_input("Ask anything about your resume")

if st.button("Send"):
    st.write("AI Response will appear here...")