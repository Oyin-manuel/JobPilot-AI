from utils.gemini import analyze_resume
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
    with st.expander("📄 View Extracted Resume Text"):
        st.text_area(
        "Extracted Text",
        resume_text,
        height=300
    )  
    
if st.button("🔍 Analyze Resume"):

    if not resume_text.strip():
        st.error("No text could be extracted from this PDF.")
    else:
        try:
            with st.spinner("Analyzing your resume..."):

                analysis = analyze_resume(resume_text)

            st.success("Analysis completed successfully!")

            st.subheader("📄 Resume Analysis")
            st.markdown(analysis)

        except Exception:
            st.error(
                "Unable to analyze the resume at the moment. Please try again in a few minutes."
            )