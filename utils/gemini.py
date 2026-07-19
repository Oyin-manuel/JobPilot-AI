import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

print("API Loaded:", os.getenv("GEMINI_API_KEY") is not None)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
    You are an expert ATS Resume Reviewer, Senior Recruiter, and Career Coach with over 15 years of experience hiring candidates across technology, business, finance, engineering, and data roles.

Your task is to analyze the resume below as if you were reviewing it for a real job application.

Evaluate the resume using the following scoring rubric:

- Formatting & Readability (15)
- Professional Summary (10)
- Technical & Soft Skills (10)
- Work Experience (20)
- Projects & Achievements (15)
- Education & Certifications (10)
- ATS Compatibility (10)
- Grammar & Professionalism (10)

Total Score = 100

Return your analysis using EXACTLY this structure:

# Overall Resume Score
Give a score out of 100 with a short explanation.

# ATS Compatibility Score
Score out of 100 and explain how ATS-friendly the resume is.

# Section Scores

Formatting:
Professional Summary:
Skills:
Experience:
Projects:
Education:
Grammar:

# Recruiter's First Impression

Write 2–3 sentences describing the first impression a recruiter would have after reading this resume.

# Top Strengths

List the strongest aspects of the resume.

# Weaknesses

Identify the biggest weaknesses.

# Missing Keywords

Mention important keywords, tools, certifications, or technologies that would improve the resume.

# ATS Issues

Point out formatting or structural issues that could reduce ATS performance.

# Bullet Point Improvements

Rewrite 3 weak resume bullet points into stronger, achievement-oriented bullet points with measurable impact where possible.

# Priority Improvements

List the top 5 improvements in order of importance.

# Recommended Job Roles

Recommend 5 suitable job roles.

For each role include:

- Match Percentage
- Reason why it matches

Example:

Data Analyst — 92%
Reason...

# Final Verdict

Conclude with a paragraph explaining whether the resume is ready for applications or what should be improved first.

Resume:

{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Error: {e}"


def generate_cover_letter(resume_text, job_description):

    prompt = f"""
You are an experienced recruiter and professional career coach.

Using ONLY the information provided in the resume and the job description, write a tailored cover letter.

Requirements:

- Use a professional business letter format.
- Write a compelling opening paragraph.
- Clearly connect the applicant's skills and experience to the job requirements.
- Do not invent qualifications or work experience.
- Keep the cover letter between 300 and 450 words.
- Use a confident but natural tone.
- Avoid generic AI phrases.
- End with a professional closing paragraph.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"