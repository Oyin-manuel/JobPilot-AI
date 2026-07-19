from utils.gemini import analyze_resume
from utils.pdf import extract_text_from_pdf
import streamlit as st

st.title("Resume Analyzer")

afile = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if afile is not None:

    st.success(f"Uploaded: {afile.name}")

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

                st.subheader("Resume Analysis")
                st.markdown(analysis)
                st.download_button(
        label="📥 Download Analysis",
                    data=analysis,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )
            except Exception as e:
                if "503" in str(e):
                    st.warning(
                        "⚠️ The AI service is currently experiencing high demand. Please try again in a few minutes."
                    )
                else:
                    st.error(f"An unexpected error occurred:\n\n{e}")