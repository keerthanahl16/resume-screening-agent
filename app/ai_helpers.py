# app/ai_helpers.py
import os
from openai import OpenAI

# Ensure API key is available
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("Missing OPENAI_API_KEY. Add it to your environment variables.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_candidate(full_text):
    prompt = f"""
    Summarize this resume into 5 bullet points:
    - Key skills
    - Experience summary
    - Strengths
    - Weaknesses
    - Job-fit summary
    
    Resume:
    {full_text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content


def explain_match(jd, resume_text):
    prompt = f"""
    Explain why this resume matches the job description.
    Provide 5 points:
    1) Skill match
    2) Experience match
    3) Missing skills
    4) Strengths
    5) Weaknesses

    Job Description:
    {jd}

    Resume:
    {resume_text}
    """
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
