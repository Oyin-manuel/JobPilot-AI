import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="JobPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 JobPilot AI")

st.subheader("Your AI Career Assistant")

st.write("""
Welcome to JobPilot AI.

This application helps job seekers:

✅ Analyze resumes
✅ Match resumes to job descriptions
✅ Generate professional cover letters
✅ Prepare for interviews
""")

uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
if uploaded_resume is not None:
     st.write("Successfully uploaded:", uploaded_resume.name)
    # Here you can add code to process the uploaded resume
else:
    st.info("Please upload your resume to proceed.")