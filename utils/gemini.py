import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(
    api_key=os.getenv("AQ.Ab8RN6J5TtWlchMCCVTP73JuoGAUBu6W1eKWwvnn7eY78XeXJw")
)

def analyze_resume(resume_text):

    prompt = f"""

You are an expert resume reviewer, career coach, and ATS (Applicant Tracking System) specialist.

Analyze the resume below and provide a professional evaluation.

Score the resume out of 100 based on:
- Resume formatting and readability
- Professional summary
- Relevant technical and soft skills
- Work experience
- Projects and achievements
- Education and certifications
- ATS compatibility
- Overall suitability for professional job applications

Provide your response using the following format:

## Resume Score
Provide a score out of 100 and briefly explain why.

## Strengths
List the strongest aspects of the resume.

## Weaknesses
Identify areas that reduce the resume's effectiveness.

## Missing Skills
Mention important skills, technologies, or certifications that could improve the candidate's chances.

## Suggested Improvements
Provide clear, practical recommendations for improving the resume.

## Recommended Job Roles
Suggest 5 job roles that best match the candidate's skills and experience.

Here is the resume:

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