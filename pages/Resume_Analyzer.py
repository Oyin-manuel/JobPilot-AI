import json
import streamlit as st

from utils.pdf import extract_text_from_pdf
from utils.gemini import analyze_resume

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.markdown("""
Upload your resume and receive an in-depth ATS analysis, recruiter feedback,
keyword optimization suggestions, and personalized career recommendations.
""")

st.divider()

resume = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if resume is not None:

    st.success(f"✅ Uploaded: {resume.name}")

    resume_text = extract_text_from_pdf(resume)

    with st.expander("📄 Preview Extracted Resume"):
        st.text_area(
            "Resume Text",
            resume_text,
            height=300
        )

    st.divider()

    if st.button("🚀 Analyze Resume", use_container_width=True):

        if not resume_text.strip():

            st.error("No readable text could be extracted from this PDF.")

        else:

            with st.spinner("🤖 AI is analyzing your resume..."):

                analysis = analyze_resume(resume_text)

            if "error" in analysis:

                st.error(analysis["error"])

            else:

                st.success("Analysis Complete!")

                st.divider()

                # =====================
                # SCORE CARDS
                # =====================

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "📄 Resume Score",
                        f'{analysis["overall_score"]}/100'
                    )

                    st.progress(
                        analysis["overall_score"] / 100
                    )

                    st.write(analysis["overall_feedback"])

                with col2:

                    st.metric(
                        "🤖 ATS Score",
                        f'{analysis["ats_score"]}/100'
                    )

                    st.progress(
                        analysis["ats_score"] / 100
                    )

                    st.write(analysis["ats_feedback"])

                st.divider()

                # =====================
                # RECRUITER IMPRESSION
                # =====================

                st.subheader("👨‍💼 Recruiter's First Impression")

                st.info(
                    analysis["recruiter_impression"]
                )

                st.divider()

                # =====================
                # STRENGTHS
                # =====================

                with st.expander("✅ Top Strengths", expanded=True):

                    for item in analysis["strengths"]:
                        st.success(item)

                # =====================
                # WEAKNESSES
                # =====================

                with st.expander("⚠ Weaknesses"):

                    for item in analysis["weaknesses"]:
                        st.warning(item)

                # =====================
                # KEYWORDS
                # =====================

                with st.expander("🏷 Missing Keywords"):

                    cols = st.columns(2)

                    for i, keyword in enumerate(
                        analysis["missing_keywords"]
                    ):

                        cols[i % 2].info(keyword)

                # =====================
                # ATS ISSUES
                # =====================

                with st.expander("🚫 ATS Issues"):

                    for issue in analysis["ats_issues"]:
                        st.error(issue)

                # =====================
                # IMPROVEMENTS
                # =====================

                with st.expander("🚀 Priority Improvements"):

                    for i, improvement in enumerate(
                        analysis["priority_improvements"],
                        start=1
                    ):

                        st.write(
                            f"**{i}.** {improvement}"
                        )

                st.divider()

                # =====================
                # RECOMMENDED JOBS
                # =====================

                st.subheader("💼 Recommended Job Roles")

                for role in analysis["recommended_roles"]:

                    with st.container(border=True):

                        st.markdown(
                            f"### {role['role']}"
                        )

                        st.progress(
                            role["match"] / 100
                        )

                        st.write(
                            f"**Match Score:** {role['match']}%"
                        )

                        st.write(
                            role["reason"]
                        )

                st.divider()

                # =====================
                # DOWNLOAD
                # =====================

                st.download_button(
                    label="📥 Download Analysis Report",
                    data=json.dumps(
                        analysis,
                        indent=4
                    ),
                    file_name="resume_analysis.json",
                    mime="application/json",
                    use_container_width=True
                )