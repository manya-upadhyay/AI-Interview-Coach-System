import streamlit as st
import re
import json
import os
import time

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

from utils.confidence_analyzer import (
    analyze_frame,
    get_confidence_result
)

from utils.speech_to_text import (
    recognize_speech,
    recognize_speech_from_audio
)

from utils.ai_helper import (
    generate_interview_questions,
    evaluate_answer,
    evaluate_interview
)

from utils.pdf_generator import generate_pdf
from database.database import save_interview


# =========================================================
# REQUIRED DIRECTORIES
# =========================================================

os.makedirs("reports", exist_ok=True)
os.makedirs("database", exist_ok=True)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HTML HELPER
# =========================================================

def html(content):
    st.html(content)



# =========================================================
# GLOBAL CSS
# =========================================================

html("""

<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 90% 5%,
            rgba(99,102,241,0.08),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #f8fafc,
            #eef2ff
        );
}

.block-container {
    max-width: 1400px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0f172a,
            #172554,
            #1e1b4b
        );

    border-right:
        1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebarNav"] a {
    border-radius: 11px;
    margin: 5px 8px;
    padding: 9px 13px;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.10);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background:
        linear-gradient(
            90deg,
            rgba(99,102,241,0.42),
            rgba(59,130,246,0.22)
        );
    font-weight: 700;
}


/* =========================================================
   HEADER
   ========================================================= */

.interview-header {
    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(129,140,248,0.35),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #0f172a,
            #172554,
            #312e81
        );

    padding: 32px 35px;
    border-radius: 23px;
    margin-bottom: 25px;

    box-shadow:
        0 18px 40px rgba(15,23,42,0.18);
}

.interview-badge {
    display: inline-block;

    padding: 7px 13px;

    border-radius: 30px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid rgba(255,255,255,0.14);

    color:
        #c7d2fe;

    font-size:
        11px;

    font-weight:
        700;

    letter-spacing:
        0.5px;

    margin-bottom:
        12px;
}

.interview-header h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin: 0 0 8px 0;
}

.interview-header p {
    color: #cbd5e1;
    font-size: 15px;
    margin: 0;
    line-height: 1.6;
}


/* =========================================================
   SECTION HEADINGS
   ========================================================= */

.section-heading {
    color: #0f172a;
    font-size: 22px;
    font-weight: 800;
    margin: 18px 0 14px 0;
}


/* =========================================================
   SETUP CARD
   ========================================================= */

.setup-card {
    background: white;

    border:
        1px solid #e2e8f0;

    border-radius: 18px;

    padding: 22px 25px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-bottom: 20px;
}

.setup-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
    margin-bottom: 5px;
}


/* =========================================================
   QUESTION CARD
   ========================================================= */

.question-card {

    background: white;

    border:
        1px solid #dbeafe;

    border-radius:
        20px;

    padding:
        30px;

    margin:
        12px 0 20px 0;

    box-shadow:
        0 12px 30px rgba(15,23,42,0.07);

    position:
        relative;
}

.question-label {

    color:
        #6366f1;

    font-size:
        12px;

    font-weight:
        800;

    letter-spacing:
        0.5px;

    margin-bottom:
        12px;
}

.question-text {

    color:
        #0f172a;

    font-size:
        21px;

    font-weight:
        700;

    line-height:
        1.55;
}


/* =========================================================
   TIMER
   ========================================================= */

.timer-card {

    background:
        #fff7ed;

    border:
        1px solid #fed7aa;

    border-radius:
        14px;

    padding:
        13px 18px;

    text-align:
        center;
}

.timer-label {

    color:
        #9a3412;

    font-size:
        11px;

    font-weight:
        700;
}

.timer-value {

    color:
        #c2410c;

    font-size:
        25px;

    font-weight:
        800;

    margin-top:
        2px;
}


/* =========================================================
   CAMERA CARD
   ========================================================= */

.camera-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        20px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-bottom:
        18px;
}


/* =========================================================
   ANSWER CARD
   ========================================================= */

.answer-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        20px 22px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-top:
        18px;
}


/* =========================================================
   VOICE CARD
   ========================================================= */

.voice-card {

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #eff6ff
        );

    border:
        1px solid #c7d2fe;

    border-radius:
        18px;

    padding:
        20px;

    margin:
        15px 0;
}

.voice-title {

    color:
        #312e81;

    font-size:
        17px;

    font-weight:
        800;

    margin-bottom:
        5px;
}

.voice-description {

    color:
        #64748b;

    font-size:
        13px;

    line-height:
        1.5;
}


/* =========================================================
   FEEDBACK CARD
   ========================================================= */

.feedback-card {

    background:
        #f8fafc;

    border:
        1px solid #cbd5e1;

    border-left:
        5px solid #6366f1;

    border-radius:
        15px;

    padding:
        20px;

    margin:
        18px 0;

    color:
        #334155;

    line-height:
        1.7;
}


/* =========================================================
   REPORT
   ========================================================= */

.report-hero {

    background:
        radial-gradient(
            circle at 85% 10%,
            rgba(129,140,248,0.30),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #0f172a,
            #1e1b4b
        );

    padding:
        32px;

    border-radius:
        22px;

    color:
        white;

    margin-bottom:
        22px;

    box-shadow:
        0 18px 40px rgba(15,23,42,0.18);
}

.report-hero h1 {

    color:
        white;

    margin:
        0 0 8px 0;

    font-size:
        30px;

    font-weight:
        800;
}

.report-hero p {

    color:
        #cbd5e1;

    margin:
        0;

    font-size:
        14px;
}


/* =========================================================
   REPORT CARDS
   ========================================================= */

.report-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        20px;

    min-height:
        120px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-bottom:
        15px;
}

.report-card-label {

    color:
        #64748b;

    font-size:
        12px;

    font-weight:
        700;
}

.report-card-value {

    color:
        #0f172a;

    font-size:
        27px;

    font-weight:
        800;

    margin-top:
        7px;
}


/* =========================================================
   LIST CARDS
   ========================================================= */

.list-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        16px;

    padding:
        15px 18px;

    margin:
        8px 0;

    color:
        #334155;

    line-height:
        1.55;
}

/* =========================================================
   COMPLETED REPORT - TEXT VISIBILITY
   ========================================================= */

.overall-score-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.overall-label {
    color: #64748b !important;
    font-size: 12px;
    font-weight: 800;
}

.overall-score {
    color: #0f172a !important;
    font-size: 42px;
    font-weight: 850;
    margin: 5px 0;
}

.overall-score span {
    color: #94a3b8 !important;
    font-size: 20px;
}

.performance-status {
    color: #475569 !important;
    font-size: 14px;
    font-weight: 700;
}

.score-description {
    color: #64748b !important;
    font-size: 13px;
    margin-top: 5px;
}

.report-metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    min-height: 110px;
    box-shadow: 0 7px 22px rgba(15,23,42,0.05);
}

.metric-title {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    margin-top: 5px;
}

.metric-number {
    color: #0f172a !important;
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}

.metric-number span {
    color: #94a3b8 !important;
    font-size: 13px;
}

.analysis-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    margin: 18px 0;
    box-shadow: 0 7px 22px rgba(15,23,42,0.05);
}

.analysis-title {
    color: #0f172a !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 15px;
}

.analysis-label {
    color: #64748b !important;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 5px;
}

.analysis-value {
    color: #0f172a !important;
    font-size: 15px;
    font-weight: 700;
}

.recommendation-card {
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    border-radius: 18px;
    padding: 22px;
    margin-top: 20px;
}

.recommendation-label {
    color: #4338ca !important;
    font-size: 12px;
    font-weight: 800;
}

.recommendation-text {
    color: #1e293b !important;
    font-size: 15px;
    line-height: 1.6;
    margin-top: 8px;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    min-height:
        46px;

    border-radius:
        11px;

    font-size:
        14px;

    font-weight:
        700;

    transition:
        all 0.22s ease;
}

.stButton > button:hover {

    transform:
        translateY(-2px);
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton > button {

    width:
        100%;

    min-height:
        48px;

    border-radius:
        12px;

    font-weight:
        700;
}


/* =========================================================
   PROGRESS
   ========================================================= */

[data-testid="stProgressBar"] {

    height:
        9px;
}

/* =========================================================
   STREAMLIT ALERT TEXT VISIBILITY
   ========================================================= */

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: #1e293b !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

[data-testid="stAlert"] {
    color: #1e293b !important;
}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    color: #1e293b !important;
}

/* =========================================================
   DOWNLOAD REPORT CARD
   ========================================================= */

.download-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 22px 25px;
    margin: 20px 0 15px 0;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.download-icon {
    font-size: 24px;
    margin-bottom: 6px;
}

.download-title {
    color: #0f172a !important;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 6px;
}

.download-text {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.6;
}

</style>
""")


# =========================================================
# VIDEO PROCESSOR
# =========================================================

class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        processed_frame, score, eye_status, smile_status = analyze_frame(img)

        return av.VideoFrame.from_ndarray(
            processed_frame,
            format="bgr24"
        )


# =========================================================
# COMPLETED REPORT
# =========================================================

def show_completed_report(report):

    # =====================================================
    # REPORT HERO
    # =====================================================

    html("""
    <div class="report-hero">

        <div class="report-badge">
            🤖 AI PERFORMANCE ANALYSIS
        </div>

        <h1>
            🎉 Interview Completed
        </h1>

        <p>
            Your AI-powered interview performance report is ready.
            Review your scores, strengths and personalized recommendations.
        </p>

    </div>
    """)


    # =====================================================
    # OVERALL SCORE
    # =====================================================

    overall_score = report.get(
        "overall_score",
        0
    )

    try:
        overall_score = float(overall_score)
    except:
        overall_score = 0


    if overall_score >= 80:

        performance_status = "Excellent Performance"
        status_icon = "🏆"

    elif overall_score >= 60:

        performance_status = "Good Performance"
        status_icon = "👍"

    else:

        performance_status = "Needs Improvement"
        status_icon = "📈"


    html(f"""
    <div class="overall-score-card">

        <div class="overall-label">
            OVERALL INTERVIEW SCORE
        </div>

        <div class="overall-score">
            {overall_score:.0f}
            <span>/100</span>
        </div>

        <div class="performance-status">
            {status_icon} {performance_status}
        </div>

        <div class="score-description">
            Based on your technical knowledge,
            problem-solving ability and communication.
        </div>

    </div>
    """)


    # =====================================================
    # SCORE BREAKDOWN
    # =====================================================

    st.markdown("### 📊 Performance Breakdown")


    technical = report.get(
        "technical",
        0
    )

    problem_solving = report.get(
        "problem_solving",
        0
    )

    communication = report.get(
        "communication",
        0
    )

    confidence = report.get(
        "confidence_score",
        report.get("confidence", 75)
    )


    score1, score2, score3, score4 = st.columns(4)


    with score1:

        html(f"""
        <div class="report-metric-card">

            <div class="metric-icon">
                💻
            </div>

            <div class="metric-title">
                TECHNICAL
            </div>

            <div class="metric-number">
                {technical}
                <span>/10</span>
            </div>

        </div>
        """)


    with score2:

        html(f"""
        <div class="report-metric-card">

            <div class="metric-icon">
                🧠
            </div>

            <div class="metric-title">
                PROBLEM SOLVING
            </div>

            <div class="metric-number">
                {problem_solving}
                <span>/10</span>
            </div>

        </div>
        """)


    with score3:

        html(f"""
        <div class="report-metric-card">

            <div class="metric-icon">
                🗣️
            </div>

            <div class="metric-title">
                COMMUNICATION
            </div>

            <div class="metric-number">
                {communication}
                <span>/10</span>
            </div>

        </div>
        """)


    with score4:

        html(f"""
        <div class="report-metric-card">

            <div class="metric-icon">
                😊
            </div>

            <div class="metric-title">
                CONFIDENCE
            </div>

            <div class="metric-number">
                {confidence}
                <span>%</span>
            </div>

        </div>
        """)


    # =====================================================
    # CONFIDENCE ANALYSIS
    # =====================================================

    eye_status = report.get(
        "eye_status",
        "Good"
    )

    smile_status = report.get(
        "smile_status",
        "Yes"
    )


    html(f"""
    <div class="analysis-card">

        <div class="analysis-title">
            😊 Confidence Analysis
        </div>

        <div class="analysis-grid">

            <div>
                <div class="analysis-label">
                    👁️ Eye Contact
                </div>

                <div class="analysis-value">
                    {eye_status}
                </div>
            </div>


            <div>
                <div class="analysis-label">
                    🙂 Facial Expression
                </div>

                <div class="analysis-value">
                    {smile_status}
                </div>
            </div>

        </div>

    </div>
    """)


    # =====================================================
    # STRENGTHS & WEAKNESSES
    # =====================================================

    strengths = report.get(
        "strengths",
        []
    )

    weaknesses = report.get(
        "weaknesses",
        []
    )


    strength_col, weakness_col = st.columns(2)


    with strength_col:

        html("""
        <div class="analysis-card">

            <div class="analysis-title">
                💪 Key Strengths
            </div>

        </div>
        """)


        if isinstance(
            strengths,
            list
        ) and strengths:

            for item in strengths:

                st.success(
                    f"✔️ {item}"
                )

        else:

            st.info(
                "No specific strengths available."
            )


    with weakness_col:

        html("""
        <div class="analysis-card">

            <div class="analysis-title">
                ⚠️ Areas for Improvement
            </div>

        </div>
        """)


        if isinstance(
            weaknesses,
            list
        ) and weaknesses:

            for item in weaknesses:

                st.warning(
                    f"⚠️ {item}"
                )

        else:

            st.info(
                "No specific improvement areas available."
            )


    # =====================================================
    # AI SUGGESTIONS
    # =====================================================

    suggestions = report.get(
        "suggestions",
        []
    )


    html("""
    <div class="analysis-card">

        <div class="analysis-title">
            💡 AI-Powered Recommendations
        </div>

        <div class="analysis-subtitle">
            Personalized suggestions based on your interview performance.
        </div>

    </div>
    """)


    if isinstance(
        suggestions,
        list
    ) and suggestions:

        for item in suggestions:

            st.info(
                f"💡 {item}"
            )

    else:

        st.info(
            "No additional suggestions available."
        )


    # =====================================================
    # FINAL RECOMMENDATION
    # =====================================================

    recommendation = report.get(
        "final_recommendation",
        "Recommended"
    )


    html(f"""
    <div class="recommendation-card">

        <div class="recommendation-label">
            🎯 FINAL AI RECOMMENDATION
        </div>

        <div class="recommendation-text">
            {recommendation}
        </div>

    </div>
    """)


    # =====================================================
    # PDF SECTION
    # =====================================================

    st.markdown("---")


    html("""
    <div class="download-card">

        <div class="download-icon">
            📄
        </div>

        <div class="download-title">
            Your Complete Interview Report
        </div>

        <div class="download-text">
            Download your detailed AI-generated performance report
            for future reference.
        </div>

    </div>
    """)


    pdf_bytes = st.session_state.get(
        "pdf_bytes"
    )


    if not pdf_bytes:

        pdf_path = st.session_state.get(
            "pdf_path",
            "reports/interview_report.pdf"
        )


        if (
            pdf_path
            and os.path.exists(pdf_path)
        ):

            with open(
                pdf_path,
                "rb"
            ) as pdf:

                pdf_bytes = pdf.read()

                st.session_state.pdf_bytes = pdf_bytes


        elif report:

            try:

                pdf_path = generate_pdf(
                    json.dumps(
                        report,
                        indent=4
                    )
                )


                with open(
                    pdf_path,
                    "rb"
                ) as pdf:

                    pdf_bytes = pdf.read()

                    st.session_state.pdf_bytes = pdf_bytes


            except Exception as e:

                print(
                    "PDF generation error:",
                    e
                )


    if pdf_bytes:

        st.download_button(
            "📄 Download Complete Report PDF",
            data=pdf_bytes,
            file_name="Interview_Report.pdf",
            mime="application/pdf",
            key="download_pdf_report_btn",
            use_container_width=True
        )


    # =====================================================
    # NEW INTERVIEW
    # =====================================================

    st.markdown("")


    if st.button(
        "🔄 Start New Interview",
        key="start_new_interview_btn",
        use_container_width=True
    ):

        st.session_state.interview_completed = False
        st.session_state.interview_report = None
        st.session_state.pdf_bytes = None
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.answers = {}


        if "report_saved" in st.session_state:

            del st.session_state.report_saved


        st.rerun()


# =========================================================
# LOGIN CHECK
# =========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.warning(
        "⚠️ Please login first."
    )

    st.switch_page(
        "pages/login.py"
    )


# =========================================================
# PAGE HEADER
# =========================================================

html("""
<div class="interview-header">

    <div class="interview-badge">
        🎯 AI-POWERED MOCK INTERVIEW
    </div>

    <h1>
        🎤 AI Mock Interview
    </h1>

    <p>
        Practice real interview scenarios with personalized AI questions,
        voice interaction, confidence tracking and intelligent feedback.
    </p>

</div>
""")


# =========================================================
# RESUME
# =========================================================

resume_text = st.session_state.get(
    "resume_text",
    ""
)


# =========================================================
# SESSION VARIABLES
# =========================================================

if "questions" not in st.session_state:
    st.session_state.questions = []


if "current_question" not in st.session_state:
    st.session_state.current_question = 0


if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = time.time()


if "answers" not in st.session_state:
    st.session_state.answers = {}


if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False


# =========================================================
# SHOW COMPLETED REPORT
# =========================================================

if (
    st.session_state.get(
        "interview_completed",
        False
    )
    and
    st.session_state.get(
        "interview_report"
    )
):

    show_completed_report(
        st.session_state.interview_report
    )

    st.stop()


# =========================================================
# INTERVIEW SETUP
# =========================================================

html("""
<div class="section-heading">
    🎯 Interview Setup
</div>
""")

html("""
<div class="setup-card">

    <div class="setup-label">
        SELECT INTERVIEW TYPE
    </div>

    <div style="
        color:#64748b;
        font-size:13px;
        line-height:1.5;
    ">
        Choose the type of interview you want to practice.
        AI will generate questions accordingly.
    </div>

</div>
""")


interview_type = st.selectbox(
    "Choose Interview Type",
    [
        "Technical Interview",
        "HR Interview",
        "Behavioral Interview",
        "Resume Based Interview",
        "Mixed Interview"
    ],
    label_visibility="collapsed"
)


st.session_state.interview_type = interview_type


# =========================================================
# RESUME CHECK
# =========================================================

if not resume_text:

    st.warning(
        "📄 Please upload your resume first before starting an interview."
    )

    if st.button(
        "📄  Go to Resume Upload",
        use_container_width=True
    ):

        st.switch_page(
            "pages/resume_upload.py"
        )

    st.stop()


# =========================================================
# GENERATE QUESTIONS
# =========================================================

if st.button(
    "🤖  Generate Interview Questions",
    use_container_width=True
):

    with st.spinner(
        "🤖 AI is analyzing your resume and preparing personalized questions..."
    ):

        try:

            questions = generate_interview_questions(
                st.session_state.interview_type,
                resume_text
            )

        except Exception as e:

            if "429" in str(e):

                st.error(
                    "⚠️ Gemini API quota exceeded. "
                    "Please try again later or use another API key."
                )

            else:

                st.error(
                    f"⚠️ {e}"
                )

            st.stop()


        st.session_state.questions = questions

        st.session_state.current_question = 0

        st.session_state.question_start_time = time.time()

        st.session_state.answers = {}

        st.session_state.interview_completed = False

        st.session_state.interview_report = None

        st.rerun()


# =========================================================
# SHOW QUESTIONS
# =========================================================

if st.session_state.questions:

    index = st.session_state.current_question

    total_questions = len(
        st.session_state.questions
    )


    # -----------------------------------------------------
    # PROGRESS HEADER
    # -----------------------------------------------------

    progress = (
        index + 1
    ) / total_questions


    pcol1, pcol2 = st.columns(
        [3, 1]
    )


    with pcol1:

        html(f"""
        <div style="
            color:#64748b;
            font-size:12px;
            font-weight:700;
            margin-bottom:6px;
        ">
            INTERVIEW PROGRESS
        </div>

        <div style="
            color:#0f172a;
            font-size:18px;
            font-weight:800;
        ">
            Question {index + 1}
            <span style="
                color:#94a3b8;
                font-weight:600;
            ">
                / {total_questions}
            </span>
        </div>
        """)


    with pcol2:

        html(f"""
        <div style="
            background:#eef2ff;
            border:1px solid #c7d2fe;
            border-radius:12px;
            padding:10px;
            text-align:center;
            color:#4338ca;
            font-size:13px;
            font-weight:800;
        ">
            {int(progress * 100)}% Complete
        </div>
        """)


    st.progress(
        progress
    )


    # -----------------------------------------------------
    # QUESTION + TIMER
    # -----------------------------------------------------

    qcol1, qcol2 = st.columns(
        [4, 1]
    )


    with qcol1:

        question = st.session_state.questions[index]

        html(f"""
        <div class="question-card">

            <div class="question-label">
                🤖 AI INTERVIEWER
            </div>

            <div class="question-text">
                {question}
            </div>

        </div>
        """)


    with qcol2:

        TIME_LIMIT = 120

        elapsed = int(
            time.time()
            -
            st.session_state.question_start_time
        )

        remaining = max(
            0,
            TIME_LIMIT - elapsed
        )

        minutes = remaining // 60

        seconds = remaining % 60


        html(f"""
        <div class="timer-card">

            <div class="timer-label">
                ⏱ TIME LEFT
            </div>

            <div class="timer-value">
                {minutes:02d}:{seconds:02d}
            </div>

        </div>
        """)


    # -----------------------------------------------------
    # TIME UP
    # -----------------------------------------------------

    if remaining == 0:

        st.warning(
            "⏰ Time's Up!"
        )

        if index < total_questions - 1:

            st.session_state.current_question += 1

            st.session_state.question_start_time = time.time()

            st.rerun()


    # -----------------------------------------------------
    # ANSWER STATE
    # -----------------------------------------------------

    if f"answer_{index}" not in st.session_state:

        st.session_state[
            f"answer_{index}"
        ] = ""


    # -----------------------------------------------------
    # CAMERA + CONFIDENCE
    # -----------------------------------------------------

    html("""
    <div class="section-heading">
        😊 Confidence Analysis
    </div>
    """)


    html("""
    <div class="camera-card">

        <div style="
            color:#0f172a;
            font-size:16px;
            font-weight:800;
            margin-bottom:5px;
        ">
            📷 Camera-Based Confidence Tracking
        </div>

        <div style="
            color:#64748b;
            font-size:13px;
            line-height:1.5;
            margin-bottom:12px;
        ">
            Enable your camera to analyze visual confidence
            indicators during the interview.
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # CAMERA CONTROL
    # -----------------------------------------------------

    if "camera_on" not in st.session_state:
        st.session_state.camera_on = False

    camera_button_text = (
        "📷 Start Camera"
        if not st.session_state.camera_on
        else "⏹ Stop Camera"
    )

    if st.button(
            camera_button_text,
            key="camera_control_btn",
            use_container_width=True
    ):
        st.session_state.camera_on = (
            not st.session_state.camera_on
        )

        st.rerun()

    if st.session_state.camera_on:
        webrtc_streamer(
            key=f"confidence-camera-{index}",
            video_processor_factory=VideoProcessor,
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
        )

    # -----------------------------------------------------
    # VOICE ANSWER
    # -----------------------------------------------------

    html("""
    <div class="section-heading">
        🎤 Your Answer
    </div>
    """)


    html("""
    <div class="voice-card">

        <div class="voice-title">
            🎙 Answer Using Your Voice
        </div>

        <div class="voice-description">
            Record your answer using your browser microphone
            or your local system microphone. Your speech will
            automatically be converted into text.
        </div>

    </div>
    """)


    # -----------------------------------------------------
    # BROWSER AUDIO
    # -----------------------------------------------------

    audio_val = st.audio_input(
        "Record your answer using Browser Mic",
        key=f"audio_input_{index}"
    )


    if audio_val is not None:

        audio_key = (
            f"transcribed_audio_{index}"
        )

        audio_id = str(
            len(
                audio_val.getvalue()
            )
        )


        if (
            st.session_state.get(
                audio_key
            )
            != audio_id
        ):

            with st.spinner(
                "🎤 Processing recording and converting voice into text..."
            ):

                speech_text = recognize_speech_from_audio(
                    audio_val
                )

                st.session_state[
                    audio_key
                ] = audio_id


                if speech_text:

                    st.session_state[
                        f"answer_{index}"
                    ] = speech_text

                    st.success(
                        "✅ Voice successfully converted to text!"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Could not recognize speech. "
                        "Please speak clearly into your microphone."
                    )


    # -----------------------------------------------------
    # LOCAL MIC
    # -----------------------------------------------------

    col_rec1, col_rec2 = st.columns(
        2
    )


    with col_rec1:

        if st.button(
            "🎤  Record via System Mic",
            key=f"record_local_{index}",
            use_container_width=True
        ):

            with st.spinner(
                "🎤 Listening via local microphone... Speak now!"
            ):

                speech_text = recognize_speech()


                if speech_text == "SYSTEM_MIC_UNAVAILABLE":

                    st.warning(
                        "⚠️ System microphone is not supported in Cloud deployment environments. "
                        "Please use the Browser Mic recording feature above."
                    )

                elif speech_text:

                    st.session_state[
                        f"answer_{index}"
                    ] = speech_text

                    st.success(
                        "✅ Voice converted to text!"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ No speech detected or local microphone unavailable."
                    )


    with col_rec2:

        html("""
        <div style="
            background:#f8fafc;
            border:1px solid #e2e8f0;
            border-radius:11px;
            padding:12px;
            text-align:center;
            color:#64748b;
            font-size:12px;
        ">
            💡 Tip: Speak clearly and explain your answer step-by-step.
        </div>
        """)


    # -----------------------------------------------------
    # TEXT ANSWER
    # -----------------------------------------------------

    answer = st.text_area(
        "Your Answer — Edit or Type Here",
        key=f"answer_{index}",
        height=180,
        placeholder="Type your interview answer here..."
    )


    # -----------------------------------------------------
    # AI EVALUATION
    # -----------------------------------------------------

    if st.button(
            "🧠  Evaluate This Answer",
            use_container_width=True
    ):

        if answer.strip() == "":

            st.warning(
                "⚠️ Please enter or record your answer first."
            )

        else:

            with st.spinner(
                    "🧠 AI is evaluating your answer and generating feedback..."
            ):

                try:

                    feedback = evaluate_answer(
                        st.session_state.questions[index],
                        answer
                    )

                except Exception:

                    st.error(
                        "⚠️ Unable to evaluate your answer right now. Please try again."
                    )

                    st.stop()

            # -----------------------------------------------------
            # FORMAT AI FEEDBACK
            # -----------------------------------------------------

            feedback_lines = feedback.splitlines()

            score_text = ""
            good_points = []
            improvement_points = []
            suggestion_points = []

            current_section = None

            for line in feedback_lines:

                line = line.strip()

                if not line:
                    continue

                lower_line = line.lower()

                # SCORE
                if lower_line.startswith("score:"):

                    score_text = line


                # WHAT WAS GOOD
                elif lower_line.startswith("what was good"):

                    current_section = "good"


                # WHAT NEEDS IMPROVEMENT
                elif (
                        lower_line.startswith("what needs improvement")
                        or
                        lower_line.startswith("what needs correction")
                ):

                    current_section = "improvement"


                # AI SUGGESTIONS
                elif (
                        lower_line.startswith("ai suggestions")
                        or
                        lower_line.startswith("ai suggestion")
                ):

                    current_section = "suggestion"


                # BULLET POINT
                elif (
                        line.startswith("-")
                        or
                        line.startswith("•")
                        or
                        line.startswith("*")
                ):

                    point = line.lstrip("-•* ").strip()

                    if current_section == "good":

                        good_points.append(point)


                    elif current_section == "improvement":

                        improvement_points.append(point)


                    elif current_section == "suggestion":

                        suggestion_points.append(point)

            # -----------------------------------------------------
            # PREPARE HTML
            # -----------------------------------------------------

            good_html = "".join(
                f"<li>{point}</li>"
                for point in good_points[:2]
            )

            improvement_html = "".join(
                f"<li>{point}</li>"
                for point in improvement_points[:2]
            )

            suggestion_html = "".join(
                f"<li>{point}</li>"
                for point in suggestion_points[:2]
            )

            # -----------------------------------------------------
            # AI FEEDBACK DISPLAY
            # -----------------------------------------------------

            html("""
            <div class="section-heading">
                🧠 AI Feedback
            </div>
            """)

            html(f"""
            <div class="feedback-card">

                <div style="
                    font-size: 22px;
                    font-weight: 700;
                    margin-bottom: 20px;
                ">
                    📊 {score_text}
                </div>


                <div style="
                    font-size: 18px;
                    font-weight: 700;
                    margin-bottom: 8px;
                ">
                    ✅ What was good
                </div>

                <ul style="
                    margin-top: 0;
                    margin-bottom: 22px;
                    padding-left: 25px;
                ">
                    {good_html}
                </ul>


                <div style="
                    font-size: 18px;
                    font-weight: 700;
                    margin-bottom: 8px;
                ">
                    ⚠️ What needs improvement
                </div>

                <ul style="
                    margin-top: 0;
                    margin-bottom: 22px;
                    padding-left: 25px;
                ">
                    {improvement_html}
                </ul>


                <div style="
                    font-size: 18px;
                    font-weight: 700;
                    margin-bottom: 8px;
                ">
                    💡 AI Suggestions
                </div>

                <ul style="
                    margin-top: 0;
                    margin-bottom: 5px;
                    padding-left: 25px;
                ">
                    {suggestion_html}
                </ul>

            </div>
            """)

    # -----------------------------------------------------
    # SAVE ANSWER
    # -----------------------------------------------------

    st.session_state.answers[index] = answer


    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    st.write("")


    nav1, nav2 = st.columns(
        2
    )


    with nav1:

        if st.button(
            "⬅️  Previous Question",
            key=f"previous_{index}",
            use_container_width=True
        ):

            if index > 0:

                st.session_state.current_question -= 1

                st.session_state.question_start_time = time.time()

                st.rerun()


    with nav2:

        if index < total_questions - 1:

            if st.button(
                "Next Question ➡️",
                key=f"next_{index}",
                use_container_width=True
            ):

                st.session_state.current_question += 1

                st.session_state.question_start_time = time.time()

                st.rerun()

        else:

            if st.button(
                "🏁  Finish Interview",
                key=f"finish_{index}",
                use_container_width=True
            ):

                report = None


                with st.spinner(
                    "📊 AI is analyzing your complete interview performance..."
                ):

                    try:

                        report = evaluate_interview(
                            st.session_state.questions,
                            st.session_state.answers
                        )

                    except Exception as e:

                        st.error(
                            f"⚠️ Unable to generate interview report: {e}"
                        )

                        st.stop()


                if report:

                    # -------------------------------------
                    # CONFIDENCE
                    # -------------------------------------

                    try:

                        confidence = get_confidence_result()

                        report[
                            "confidence_score"
                        ] = confidence["score"]

                        report[
                            "eye_status"
                        ] = confidence["eye_status"]

                        report[
                            "smile_status"
                        ] = confidence["smile_status"]

                    except Exception:

                        report[
                            "confidence_score"
                        ] = 75

                        report[
                            "eye_status"
                        ] = "Good"

                        report[
                            "smile_status"
                        ] = "Yes"


                    # -------------------------------------
                    # SCORE
                    # -------------------------------------

                    score = report.get(
                        "overall_score",
                        0
                    )


                    # -------------------------------------
                    # SAVE DATABASE
                    # -------------------------------------

                    if (
                        "report_saved"
                        not in st.session_state
                    ):

                        try:

                            user_email = (
                                st.session_state.get("email")
                                or
                                st.session_state.get("user")
                                or
                                "candidate@example.com"
                            )


                            save_interview(
                                user_email,
                                score,
                                json.dumps(
                                    report,
                                    indent=4
                                )
                            )


                            st.session_state.report_saved = True


                        except Exception as db_err:

                            print(
                                "DB save warning:",
                                db_err
                            )


                    # -------------------------------------
                    # PDF
                    # -------------------------------------

                    try:

                        pdf_path = generate_pdf(
                            json.dumps(
                                report,
                                indent=4
                            )
                        )


                        st.session_state.pdf_path = pdf_path


                        with open(
                            pdf_path,
                            "rb"
                        ) as f:

                            st.session_state.pdf_bytes = f.read()


                    except Exception as pdf_err:

                        print(
                            "PDF generation warning:",
                            pdf_err
                        )


                    # -------------------------------------
                    # FINAL STATE
                    # -------------------------------------

                    st.session_state.interview_report = report

                    st.session_state.interview_completed = True

                    st.rerun()