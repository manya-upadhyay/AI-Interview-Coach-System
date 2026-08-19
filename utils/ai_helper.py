import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY


def handle_gemini_error(e):
    error = str(e)
    if "429" in error:
        return "⚠️ Gemini API quota exceeded. Please try again later or configure another API key."
    if "503" in error:
        return "⚠️ Gemini AI service is temporarily unavailable. Please try again shortly."
    if "401" in error or "API key" in error.lower():
        return "⚠️ Gemini API key is missing or invalid."
    return f"⚠️ {error}"


def _model():
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is not configured. Add GEMINI_API_KEY to Streamlit Secrets.")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-2.5-flash")


def _parse_json(text):
    text = (text or "").strip().replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return json.loads(match.group(0) if match else text)


def analyze_resume(resume_text):
    prompt = f"""
You are an expert HR recruiter and ATS Resume Analyzer.
Analyze this resume and return ONLY valid JSON with exactly these keys:
{{"candidate_name":"","email":"","skills":[],"education":[],"projects":[],"experience":"","strengths":[],"weaknesses":[],"resume_score":0,"ats_score":0,"missing_skills":[],"career_recommendation":"","suggestions":[]}}
Resume:
{resume_text}
"""
    try:
        return _parse_json(_model().generate_content(prompt).text)
    except Exception as e:
        return {"candidate_name":"","email":"","skills":[],"education":[],"projects":[],"experience":"",
                "strengths":[],"weaknesses":[],"resume_score":0,"ats_score":0,"missing_skills":[],
                "career_recommendation":"","suggestions":[handle_gemini_error(e)]}


def evaluate_answer(question, answer):
    prompt = f"""You are an expert technical interviewer.
Question: {question}
Candidate Answer: {answer}
Evaluate with Score (out of 10), Strengths, Weaknesses, and Improved Answer."""
    try:
        return _model().generate_content(prompt).text
    except Exception as e:
        return handle_gemini_error(e)


def evaluate_interview(questions, answers):
    qa = "\n".join(f"Question {i+1}:\n{q}\nAnswer:\n{answers.get(i) or answers.get(str(i)) or ''}\n" for i, q in enumerate(questions))
    prompt = f"""You are an expert HR interviewer. Evaluate this interview and return ONLY valid JSON:
{{"overall_score":0,"technical":0,"communication":0,"problem_solving":0,"confidence":0,"strengths":[],"weaknesses":[],"suggestions":[],"final_recommendation":""}}
Interview:
{qa}"""
    try:
        return _parse_json(_model().generate_content(prompt).text)
    except Exception as e:
        return {"overall_score":0,"technical":0,"communication":0,"problem_solving":0,"confidence":0,
                "strengths":[handle_gemini_error(e)],"weaknesses":[],"suggestions":[],"final_recommendation":""}


def generate_interview_questions(interview_type, resume_text):
    prompt = f"""You are an expert interviewer.
Interview Type: {interview_type}
Candidate Resume: {resume_text}
Generate exactly 10 relevant interview questions. Return one question per line, with no numbering or explanation."""
    try:
        questions = [q.strip() for q in _model().generate_content(prompt).text.splitlines() if q.strip()]
        return [re.sub(r"^\s*(?:\d+[.)]|[-•])\s*", "", q).strip() for q in questions][:10]
    except Exception as e:
        raise Exception(handle_gemini_error(e))
