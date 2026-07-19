import streamlit as st

from utils.pdf import extract_text_from_pdf
from utils.gemini import generate_cover_letter

st.title("✍️ Cover Letter Generator")

st.write(
    "Generate a personalized cover letter tailored to a specific job description."
)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder="Paste the full job description here..."
)

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    resume_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 Resume Preview"):
        st.text_area(
            "Extracted Resume",
            resume_text,
            height=250
        )

    if st.button("✍️ Generate Cover Letter"):

        if not job_description.strip():
            st.warning("Please paste a job description first.")

        else:

            with st.spinner("Generating your cover letter..."):

                cover_letter = generate_cover_letter(
                    resume_text,
                    job_description
                )

            st.subheader("Generated Cover Letter")

            st.markdown(cover_letter)

            st.download_button(
                label="📥 Download Cover Letter",
                data=cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain"
            )