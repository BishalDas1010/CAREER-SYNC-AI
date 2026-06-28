import streamlit as st
import requests
st.title("CAREER-SYNC-AI")

#need to upload the Resume 
uploaded_resume = st.file_uploader("Upload the resume file",type="pdf")
uploaded_job =st.file_uploader("upload the job describtion",type="txt")

if st.button("Analyze"):
    files = {
        "resume_file": uploaded_resume,
        "job_file": uploaded_job,
    }
    response = requests.post("http://localhost:8000/upload", files=files)
    data = response.json()
    st.session_state.session_id = data["session_id"]
    st.write(data["analysis"])
    question = st.text_input("Ask a follow-up question")
if st.button("Ask"):
    resp = requests.post("http://localhost:8000/chat", data={
        "session_id": st.session_state.session_id,
        "question": question,
    })
    st.write(resp.json()["answer"])
