import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

print("API Loaded:", os.getenv("GEMINI_API_KEY") is not None)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ==========================
# Resume Analyzer
# ==========================

def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer and Senior Recruiter.

Analyze the resume below.

Return ONLY valid JSON.

Do NOT wrap the response inside markdown.
Do NOT include ```json.

Use this exact schema:

{{
  "overall_score": 0,
  "overall_feedback": "",

  "ats_score": 0,
  "ats_feedback": "",

  "recruiter_impression": "",

  "strengths": [
    "",
    "",
    ""
  ],

  "weaknesses": [
    "",
    "",
    ""
  ],

  "missing_keywords": [
    "",
    "",
    ""
  ],

  "ats_issues": [
    "",
    ""
  ],

  "priority_improvements": [
    "",
    "",
    "",
    "",
    ""
  ],

  "recommended_roles": [
    {{
      "role": "",
      "match": 0,
      "reason": ""
    }}
  ]
}}

Resume:

{resume_text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}


# ==========================
# Cover Letter Generator
# ==========================

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
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"


# ==========================
# Job Matcher
# ==========================

def match_resume_to_job(resume_text, job_description):

    prompt = f"""
You are an expert ATS recruiter, hiring manager, and career coach.

Compare the candidate's resume against the job description.

Return ONLY valid JSON.

Do NOT wrap the response in markdown.
Do NOT include ```json.

Use this exact schema:

{{
    "overall_match_score": 0,
    "overall_feedback": "",

    "ats_score": 0,
    "ats_feedback": "",

    "matching_skills": [
        "",
        "",
        "",
        "",
        ""
    ],

    "missing_skills": [
        "",
        "",
        "",
        "",
        ""
    ],

    "missing_keywords": [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ],

    "strengths": [
        "",
        "",
        "",
        "",
        ""
    ],

    "weaknesses": [
        "",
        "",
        "",
        "",
        ""
    ],

    "resume_improvements": [
        "",
        "",
        "",
        "",
        ""
    ],

    "hiring_recommendation": {{
        "decision": "",
        "reason": ""
    }}
}}

Resume:

{resume_text}

Job Description:

{job_description}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {
            "error": str(e)
        }