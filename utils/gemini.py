import json
import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from google import genai


# Load variables from the local .env file.
# On Streamlit Cloud, the key will come from st.secrets instead.
load_dotenv()

MODEL_NAME = "gemini-3.6-flash"


def get_api_key() -> str:
    """
    Get the Gemini API key from either:
    1. The local .env file
    2. Streamlit Community Cloud secrets
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key.strip()

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if api_key:
            return str(api_key).strip()

    except Exception:
        pass

    raise RuntimeError(
        "GEMINI_API_KEY was not found. "
        "Add it to your local .env file or Streamlit Cloud secrets."
    )


def get_client() -> genai.Client:
    """
    Create and return a Gemini client.
    """

    return genai.Client(api_key=get_api_key())


def clean_json_response(text: str) -> str:
    """
    Remove Markdown code fences that Gemini may add around JSON.
    """

    cleaned_text = text.strip()

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[len("```json"):].strip()

    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[len("```"):].strip()

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3].strip()

    return cleaned_text


def generate_text(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()


# =========================================================
# Resume Analyzer
# =========================================================

def analyze_resume(resume_text: str) -> dict[str, Any]:
    """
    Analyze a resume and return structured JSON data.
    """

    if not resume_text or not resume_text.strip():
        return {"error": "The resume text is empty."}

    prompt = f"""
You are an expert ATS resume reviewer and senior recruiter.

Analyze the resume provided below.

Return ONLY valid JSON.

Do not wrap the response in Markdown.
Do not include ```json or any other code fences.
Do not include any explanation outside the JSON object.

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

Scoring rules:

- All scores must be numbers from 0 to 100.
- Give specific feedback based only on the resume.
- Do not invent qualifications, skills, education, projects, or experience.
- Recommended roles must be realistic for the candidate.
- Return at least three recommended roles when enough information is available.
- Keep every list item clear and practical.

Resume:

{resume_text}
"""

    try:
        response_text = generate_text(prompt)
        cleaned_text = clean_json_response(response_text)
        result = json.loads(cleaned_text)

        if not isinstance(result, dict):
            return {
                "error": "Gemini returned an unexpected response format."
            }

        return result

    except json.JSONDecodeError:
        return {
            "error": (
                "Gemini returned a response that could not be parsed as JSON. "
                "Please try again."
            )
        }

    except Exception as error:
        return {"error": str(error)}


# =========================================================
# Cover Letter Generator
# =========================================================

def generate_cover_letter(
    resume_text: str,
    job_description: str,
) -> str:
    """
    Generate a tailored cover letter from a resume and job description.
    """

    if not resume_text or not resume_text.strip():
        return "Error: The resume text is empty."

    if not job_description or not job_description.strip():
        return "Error: The job description is empty."

    prompt = f"""
You are an experienced recruiter and professional career coach.

Using only the information provided in the resume and job description,
write a tailored cover letter for the applicant.

Requirements:

- Use a professional business-letter style.
- Write a compelling opening paragraph.
- Clearly connect the applicant's genuine skills, education, projects,
  and experience to the job requirements.
- Do not invent qualifications, achievements, employers, experience,
  responsibilities, certifications, or statistics.
- Keep the cover letter between 300 and 450 words.
- Use a confident, natural, and professional tone.
- Avoid generic AI phrases and exaggerated claims.
- Avoid repeating the resume word for word.
- Do not use Markdown headings.
- Do not include placeholders such as "[Company Name]" unless the
  company name is unavailable.
- End with a professional closing paragraph.
- Finish with "Sincerely," but do not invent the applicant's name.

Resume:

{resume_text}

Job Description:

{job_description}
"""

    try:
        return generate_text(prompt)

    except Exception as error:
        return f"Error: {error}"


# =========================================================
# Job Matcher
# =========================================================

def match_resume_to_job(
    resume_text: str,
    job_description: str,
) -> str:
    """
    Compare a resume with a job description and return a Markdown report.
    """

    if not resume_text or not resume_text.strip():
        return "Error: The resume text is empty."

    if not job_description or not job_description.strip():
        return "Error: The job description is empty."

    prompt = f"""
You are an expert ATS recruiter, hiring manager, and career coach.

Compare the candidate's resume with the job description.

Evaluate the candidate exactly as a recruiter would.

Base every conclusion only on the information supplied.
Do not invent qualifications, employment history, skills, projects,
certifications, achievements, or experience.

Return the answer in Markdown using exactly this structure:

# Overall Match Score

Give a score out of 100 and explain the main reasons for the score.

# ATS Compatibility

Give a score out of 100 and explain how well the resume is likely
to perform in an applicant tracking system for this role.

# Matching Skills

List the resume skills, experience, education, and qualifications
that clearly match the job description.

# Missing Skills

List important required or preferred skills that are not demonstrated
in the resume.

# Missing Keywords

List relevant job-description keywords that are genuinely applicable
and could be added to the resume if the candidate actually possesses
those skills or experiences.

# Strengths

Highlight the candidate's strongest qualifications for this role.

# Weaknesses

Explain the biggest gaps or concerns a recruiter may notice.

# Resume Improvements

Give specific, practical recommendations for tailoring the resume
to this particular role.

# Hiring Recommendation

Choose exactly one:

- Strong Match
- Moderate Match
- Weak Match

Explain the reasoning clearly.

Resume:

{resume_text}

Job Description:

{job_description}
"""

    try:
        return generate_text(prompt)

    except Exception as error:
        return f"Error: {error}"