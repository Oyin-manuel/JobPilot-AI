import streamlit as st

st.set_page_config(
    page_title="JobPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------- CUSTOM CSS ----------

st.markdown("""
<style>

.main{
    padding-top:2rem;
}

.hero{
    background: linear-gradient(135deg,#2563eb,#4f46e5);
    padding:40px;
    border-radius:18px;
    color:white;
    text-align:center;
    margin-bottom:30px;
}

.hero h1{
    font-size:48px;
    margin-bottom:10px;
}

.hero p{
    font-size:20px;
    color:#e5e7eb;
}

.feature-card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0px 4px 15px rgba(0,0,0,.08);
    border-left:6px solid #2563eb;
    margin-bottom:20px;
    transition:.3s;
}

.feature-card:hover{
    transform:translateY(-5px);
    box-shadow:0px 10px 30px rgba(0,0,0,.15);
}

.feature-title{
    font-size:24px;
    font-weight:bold;
    color:#2563eb;
}

.metric-card{
    background:#f8fafc;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:1px solid #e5e7eb;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------

st.markdown("""
<div class="hero">

<h1>🚀 JobPilot AI</h1>

<p>
Navigate Your Career with Confidence
</p>

<p>
AI-powered tools that help you analyze resumes,
generate professional cover letters,
and land more interviews.
</p>

</div>
""", unsafe_allow_html=True)

# ---------- FEATURES ----------

st.header("✨ Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
<div class="feature-card">

<div class="feature-title">
📄 Resume Analyzer
</div>

<br>

✔ ATS Resume Score

✔ Recruiter Feedback

✔ Resume Improvements

✔ Resume Strengths & Weaknesses

✔ Recommended Job Roles

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">

<div class="feature-title">
🎯 AI Job Matcher
</div>

<br>

✔ Match Percentage

✔ Missing Keywords

✔ Skill Gap Analysis

✔ Hiring Recommendation

</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="feature-card">

<div class="feature-title">
📝 Cover Letter Generator
</div>

<br>

✔ Personalized Cover Letters

✔ Professional Formatting

✔ ATS Friendly

✔ Ready to Download

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature-card">

<div class="feature-title">
🎤 Interview Preparation
</div>

<br>

Coming Soon

AI-generated interview questions with personalized feedback.

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------- METRICS ----------

st.header("📊 Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("AI Features", "3")

with c2:
    st.metric("Powered By", "Gemini 3.6 Flash")

with c3:
    st.metric("Version", "1.0")

st.divider()

# ---------- ROADMAP ----------

st.header("🛣 Product Roadmap")

st.progress(50)

st.write("✅ Resume Analyzer")
st.write("✅ Cover Letter Generator")
st.write("✅ AI Job Matcher")
st.write("🔄 Interview Preparation")
st.write("🔄 AI Job Search")
st.write("🔄 Career Dashboard")

st.divider()

st.success("👈 Select a feature from the sidebar to get started.")

st.markdown("""
<div class="footer">

Built by Hans Shaibu

Powered by Google Gemini AI

</div>
""", unsafe_allow_html=True)