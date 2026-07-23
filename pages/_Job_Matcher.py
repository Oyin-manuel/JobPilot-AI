import streamlit as st
import json

from utils.pdf import extract_text_from_pdf
from utils.gemini import match_resume_to_job

st.set_page_config(
    page_title="Job Matcher",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Job Matcher")

st.write(
    "Upload your resume and compare it against a job description to see how well you match."
)

st.divider()

resume = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=250
)

if resume is not None:

    st.success(f"✅ Uploaded: {resume.name}")

    resume_text = extract_text_from_pdf(resume)

    with st.expander("📄 View Extracted Resume"):
        st.text_area(
            "Resume",
            resume_text,
            height=250
        )

st.divider()

if st.button("🚀 Match Resume", use_container_width=True):

    if resume is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please paste the job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            analysis = match_resume_to_job(
                resume_text,
                job_description
            )

        # Error returned from Gemini
        if isinstance(analysis, dict) and "error" in analysis:
            st.error(analysis["error"])

        # JSON response
        elif isinstance(analysis, dict):

            st.success("Analysis Complete!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Overall Match",
                    f'{analysis["overall_match_score"]}/100'
                )
                st.progress(
                    analysis["overall_match_score"] / 100
                )

            with col2:
                st.metric(
                    "ATS Compatibility",
                    f'{analysis["ats_score"]}/100'
                )
                st.progress(
                    analysis["ats_score"] / 100
                )

            st.divider()

            st.subheader("📌 Overall Feedback")
            st.write(analysis["overall_feedback"])

            st.subheader("🤖 ATS Feedback")
            st.write(analysis["ats_feedback"])

            with st.expander("✅ Matching Skills", expanded=True):
                for item in analysis["matching_skills"]:
                    st.success(item)

            with st.expander("❌ Missing Skills"):
                for item in analysis["missing_skills"]:
                    st.warning(item)

            with st.expander("🏷 Missing Keywords"):
                cols = st.columns(2)

                for i, item in enumerate(analysis["missing_keywords"]):
                    cols[i % 2].info(item)

            with st.expander("💪 Strengths"):
                for item in analysis["strengths"]:
                    st.success(item)

            with st.expander("⚠ Weaknesses"):
                for item in analysis["weaknesses"]:
                    st.warning(item)

            with st.expander("🚀 Resume Improvements"):
                for i, item in enumerate(
                    analysis["resume_improvements"],
                    start=1
                ):
                    st.write(f"**{i}.** {item}")

            st.subheader("👔 Hiring Recommendation")

            decision = analysis["hiring_recommendation"]["decision"]

            if decision.lower() == "strong match":
                st.success(decision)

            elif decision.lower() == "moderate match":
                st.warning(decision)

            else:
                st.error(decision)

            st.write(
                analysis["hiring_recommendation"]["reason"]
            )

            st.download_button(
                "📥 Download Report",
                data=json.dumps(
                    analysis,
                    indent=4
                ),
                file_name="job_match_report.json",
                mime="application/json",
                use_container_width=True
            )

        # Markdown fallback
        else:

            st.markdown(analysis)

            st.download_button(
                "📥 Download Report",
                data=str(analysis),
                file_name="job_match_report.txt",
                mime="text/plain",
                use_container_width=True
            )