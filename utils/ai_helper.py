import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY

def handle_gemini_error(e):

    error = str(e)

    if "429" in error:
        return (
            "⚠️ Gemini API quota exceeded.\n\n"
            "Please try again later or use another API key."
        )

    elif "503" in error:
        return (
            "⚠️ Gemini AI service is temporarily unavailable.\n\n"
            "Please try again after some time."
        )

    elif "401" in error:
        return (
            "⚠️ Invalid Gemini API Key."
        )

    else:
        return f"⚠️ {error}"

def get_model():
    from config import GEMINI_API_KEY
    key = GEMINI_API_KEY
    if not key:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    if not key:
        raise Exception("Gemini API Key is not set. Please configure GEMINI_API_KEY in Streamlit Secrets or .env file.")

    genai.configure(api_key=key)
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for m in models:
        try:
            return genai.GenerativeModel(m)
        except Exception:
            continue
    return genai.GenerativeModel("gemini-1.5-flash")


def analyze_resume(resume_text):

    prompt = f"""
You are an expert HR recruiter and ATS Resume Analyzer.

Analyze the following resume.

Return ONLY valid JSON.

Format:

{{
    "candidate_name":"",
    "email":"",
    "skills":[],
    "education":[],
    "projects":[],
    "experience":"",
    "strengths":[],
    "weaknesses":[],
    "resume_score":0,
    "ats_score":0,
    "missing_skills":[],
    "career_recommendation":"",
    "suggestions":[]
}}

Rules:

- Do not write markdown.
- Do not write explanation.
- Do not use ```json.
- Return ONLY JSON.

Resume:

{resume_text}
"""

    try:

        response = get_model().generate_content(prompt)

        text = response.text.strip()

        # Remove markdown if present
        text = text.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            text = match.group(0)

        return json.loads(text)

    except Exception as e:

        return {
            "candidate_name":"",
            "email":"",
            "skills":[],
            "education":[],
            "projects":[],
            "experience":"",
            "strengths":[],
            "weaknesses":[],
            "resume_score":0,
            "ats_score":0,
            "missing_skills":[],
            "career_recommendation":"",
            "suggestions": [handle_gemini_error(e)]
        }

def evaluate_answer(question, answer):

    prompt = f"""
You are an AI Interview Coach.

Evaluate the candidate's answer ONLY according to the interview question.

Question:
{question}

Candidate's Answer:
{answer}

Give concise, specific and practical feedback.

STRICT RULES:
- Give a fair score from 0 to 10.
- Do not explain the complete topic.
- Do not repeat the question.
- Do not invent information.
- Do not give generic feedback.
- Focus only on the candidate's actual answer.
- Use maximum 2 points in each section.
- Every point must be a short sentence.
- Do not write paragraphs.

Return ONLY this exact format:

Score: <score>/10

What was good:
- <short point>
- <short point>

What needs improvement:
- <short point>
- <short point>

AI Suggestions:
- <short actionable point>
- <short actionable point>

IMPORTANT:
The "AI Suggestions" section MUST contain exactly 2 bullet points.
Never leave the AI Suggestions section empty.
    """

    try:

        response = get_model().generate_content(prompt)

        return response.text.strip()

    except Exception as e:

        return handle_gemini_error(e)


def evaluate_interview(questions, answers):

    qa = ""

    for i in range(len(questions)):
        answer_text = answers.get(i) or answers.get(str(i)) or ""
        qa += f"""
Question {i+1}:
{questions[i]}

Answer:
{answer_text}

"""


    prompt = f"""
You are an expert HR interviewer.

Evaluate the interview.

Interview:

{qa}

Return ONLY valid JSON.

Format:

{{
    "overall_score": 0,
    "technical": 0,
    "communication": 0,
    "problem_solving": 0,
    "confidence": 0,
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "final_recommendation": ""
}}

Rules:

- Return only JSON.
- Do not use markdown.
- Do not explain anything.
"""

    try:

        response = get_model().generate_content(prompt)

        text = response.text.strip()

        text = text.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            text = match.group(0)

        return json.loads(text)

    except Exception as e:

        return {
            "overall_score":0,
            "technical":0,
            "communication":0,
            "problem_solving":0,
            "confidence":0,
            "strengths": [handle_gemini_error(e)],
            "weaknesses":[],
            "suggestions":[],
            "final_recommendation":""
        }

def generate_interview_questions(interview_type, resume_text):

    prompt = f"""
You are an expert interviewer.

Interview Type:
{interview_type}

Candidate Resume:

{resume_text}

Generate exactly 10 interview questions.

Rules:
- Questions must match the selected interview type.
- One question per line.
- No numbering.
- No explanation.
- No headings.
- Keep questions relevant to the candidate's resume.
"""

    try:
        response = get_model().generate_content(prompt)

        questions = response.text.split("\n")
        questions = [q.strip() for q in questions if q.strip()]

        return questions

    except Exception as e:
        raise Exception(str(e))