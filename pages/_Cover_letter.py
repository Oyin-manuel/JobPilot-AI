import streamlit as st

from utils.pdf import (
    extract_text_from_pdf,
    create_cover_letter_pdf
)

from utils.gemini import generate_cover_letter


st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ AI Cover Letter Generator")

st.write(
    "Generate a professional cover letter tailored specifically to your chosen job."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)

if uploaded_file is not None:

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    resume_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 Resume Preview"):

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=250
        )

st.divider()

if st.button(
    "🚀 Generate Cover Letter",
    use_container_width=True
):

    if uploaded_file is None:

        st.error(
            "Please upload your resume."
        )

    elif not job_description.strip():

        st.error(
            "Please paste the job description."
        )

    else:

        with st.spinner(
            "🤖 Writing your personalized cover letter..."
        ):

            cover_letter = generate_cover_letter(
                resume_text,
                job_description
            )

        if cover_letter.startswith("Error"):

            st.error(cover_letter)

        else:

            pdf_file = create_cover_letter_pdf(
                cover_letter
            )

            st.success(
                "✅ Cover Letter Generated Successfully!"
            )

            st.divider()

            st.subheader("📄 Generated Cover Letter")

            st.markdown(
                f"""
<div style="
background-color:#f8f9fa;
padding:30px;
border-radius:12px;
border:1px solid #dddddd;
line-height:1.8;
font-size:16px;
white-space:pre-wrap;
">

{cover_letter}

</div>
""",
                unsafe_allow_html=True
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(
                    label="📥 Download TXT",
                    data=cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:

                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_file,
                    file_name="cover_letter.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )