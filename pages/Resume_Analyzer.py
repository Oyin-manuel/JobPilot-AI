import pandas as pd
import streamlit as st
import pymupdf as fitz  # PyMuPDF
def extract_text_from_pdf(uploaded_file):
     pdf_bytes = uploaded_file.getvalue()
     doc = fitz.open(stream = pdf_bytes, filetype = "pdf")
     
     texts = []
     
     for page in doc:
        text = page.get_text()
        texts.append(text)
        
     full_text = "\n".join(texts)
     
     return full_text
 
 
 #
st.title("Resume Analyzer")
afile = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if afile is not None:
    st.write("Successfully uploaded:", afile.name)
    resume_text = extract_text_from_pdf(afile)
    st.text_area("Extracted Resume Text", resume_text, height=300)