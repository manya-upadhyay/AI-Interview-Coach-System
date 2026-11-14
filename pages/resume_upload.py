import streamlit as st
import os

from utils.ai_helper import analyze_resume
from utils.resume_parser import extract_text


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Resume Analysis | AI Interview Coach",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# HTML HELPER
# =========================================================

def html(content):
    st.html(content)


# =========================================================
# CUSTOM CSS
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

    max-width:
        1400px;

    padding-top:
        1.8rem;

    padding-bottom:
        3rem;
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
}


[data-testid="stSidebar"] * {
    color: white;
}


[data-testid="stSidebarNav"] a {

    border-radius:
        11px;

    margin:
        5px 8px;

    padding:
        9px 13px;
}


[data-testid="stSidebarNav"] a:hover {

    background:
        rgba(255,255,255,0.10);
}


[data-testid="stSidebarNav"] a[aria-current="page"] {

    background:
        linear-gradient(
            90deg,
            rgba(99,102,241,0.42),
            rgba(59,130,246,0.22)
        );

    font-weight:
        700;
}


/* =========================================================
   HEADER
   ========================================================= */

.resume-header {

    background:
        radial-gradient(
            circle at 85% 10%,
            rgba(129,140,248,0.35),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #0f172a,
            #172554,
            #312e81
        );

    padding:
        32px 35px;

    border-radius:
        23px;

    margin-bottom:
        25px;

    box-shadow:
        0 18px 40px rgba(15,23,42,0.18);
}


.resume-badge {

    display:
        inline-block;

    padding:
        7px 13px;

    border-radius:
        30px;

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


.resume-header h1 {

    color:
        white;

    font-size:
        36px;

    font-weight:
        800;

    margin:
        0 0 8px 0;
}


.resume-header p {

    color:
        #cbd5e1;

    font-size:
        15px;

    margin:
        0;

    line-height:
        1.6;
}


/* =========================================================
   UPLOAD CARD
   ========================================================= */

.upload-card {

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid #e2e8f0;

    border-radius:
        20px;

    padding:
        25px;

    margin-bottom:
        20px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}


.upload-title {

    color:
        #0f172a;

    font-size:
        20px;

    font-weight:
        800;

    margin-bottom:
        5px;
}


.upload-subtitle {

    color:
        #64748b;

    font-size:
        13px;

    margin-bottom:
        18px;
}


/* =========================================================
   INFO CARDS
   ========================================================= */

.info-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        16px;

    padding:
        18px;

    height:
        100%;

    box-shadow:
        0 7px 20px rgba(15,23,42,0.04);
}


.info-icon {

    font-size:
        23px;

    margin-bottom:
        8px;
}


.info-title {

    color:
        #0f172a;

    font-size:
        15px;

    font-weight:
        800;

    margin-bottom:
        5px;
}


.info-text {

    color:
        #64748b;

    font-size:
        12px;

    line-height:
        1.5;
}


/* =========================================================
   SCORE CARDS
   ========================================================= */

.score-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        22px;

    text-align:
        center;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
}


.score-label {

    color:
        #64748b;

    font-size:
        12px;

    font-weight:
        700;

    letter-spacing:
        0.4px;
}


.score-value {

    color:
        #0f172a;

    font-size:
        34px;

    font-weight:
        850;

    margin:
        5px 0;
}


.score-desc {

    color:
        #94a3b8;

    font-size:
        11px;
}


/* =========================================================
   SECTION CARD
   ========================================================= */

.section-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        22px;

    margin:
        18px 0;

    box-shadow:
        0 7px 22px rgba(15,23,42,0.04);
}


.section-title {

    color:
        #0f172a;

    font-size:
        18px;

    font-weight:
        800;

    margin-bottom:
        15px;
}


/* =========================================================
   TAGS
   ========================================================= */

.skill-tag {

    display:
        inline-block;

    background:
        #eef2ff;

    color:
        #3730a3;

    border:
        1px solid #c7d2fe;

    border-radius:
        30px;

    padding:
        7px 12px;

    margin:
        4px;

    font-size:
        12px;

    font-weight:
        700;
}


.missing-tag {

    display:
        inline-block;

    background:
        #fff7ed;

    color:
        #c2410c;

    border:
        1px solid #fed7aa;

    border-radius:
        30px;

    padding:
        7px 12px;

    margin:
        4px;

    font-size:
        12px;

    font-weight:
        700;
}


/* =========================================================
   CANDIDATE CARD
   ========================================================= */

.candidate-card {

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #f8fafc
        );

    border:
        1px solid #c7d2fe;

    border-radius:
        17px;

    padding:
        20px;
}


.candidate-label {

    color:
        #64748b;

    font-size:
        11px;

    font-weight:
        700;

    margin-top:
        8px;
}


.candidate-value {

    color:
        #0f172a;

    font-size:
        15px;

    font-weight:
        700;
}
/* =========================================================
   ALERT TEXT VISIBILITY
   ========================================================= */

[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: #1e293b !important;
}

[data-testid="stAlert"] {
    font-size: 14px;
}

[data-testid="stAlert"] svg {
    opacity: 1 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    min-height:
        46px;

    border-radius:
        12px;

    font-weight:
        700;

    transition:
        all 0.2s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);
}


/* =========================================================
   FOOTER
   ========================================================= */

.resume-footer {

    text-align:
        center;

    color:
        #94a3b8;

    font-size:
        12px;

    margin-top:
        35px;
}

</style>
""")


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
# HEADER
# =========================================================

html("""
<div class="resume-header">

    <div class="resume-badge">
        🤖 AI-POWERED RESUME ANALYSIS
    </div>

    <h1>
        📄 Resume Analysis
    </h1>

    <p>
        Upload your resume and let AI evaluate your profile,
        skills, ATS compatibility and career readiness.
    </p>

</div>
""")


# =========================================================
# UPLOAD SECTION
# =========================================================

html("""
<div class="upload-card">

    <div class="upload-title">
        📤 Upload Your Resume
    </div>

    <div class="upload-subtitle">
        Supported formats: PDF and DOCX
    </div>

</div>
""")


uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    label_visibility="collapsed"
)


# =========================================================
# QUICK INFO
# =========================================================

if not uploaded_file:

    st.markdown("### Why analyze your resume?")


    c1, c2, c3 = st.columns(3)


    with c1:

        html("""
        <div class="info-card">

            <div class="info-icon">
                🎯
            </div>

            <div class="info-title">
                Resume Score
            </div>

            <div class="info-text">
                Understand how strong your resume is
                for your target career.
            </div>

        </div>
        """)


    with c2:

        html("""
        <div class="info-card">

            <div class="info-icon">
                🔎
            </div>

            <div class="info-title">
                ATS Compatibility
            </div>

            <div class="info-text">
                Identify how well your resume performs
                against ATS screening.
            </div>

        </div>
        """)


    with c3:

        html("""
        <div class="info-card">

            <div class="info-icon">
                💡
            </div>

            <div class="info-title">
                AI Recommendations
            </div>

            <div class="info-text">
                Get personalized suggestions to
                improve your resume.
            </div>

        </div>
        """)


# =========================================================
# PROCESS UPLOADED RESUME
# =========================================================

if uploaded_file:

    os.makedirs(
        "uploads",
        exist_ok=True
    )


    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )


    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )


    # -----------------------------------------------------
    # UPLOAD SUCCESS
    # -----------------------------------------------------

    html(f"""
    <div style="
        background:#ecfdf5;
        border:1px solid #a7f3d0;
        border-radius:14px;
        padding:14px 18px;
        margin:15px 0;
    ">

        <div style="
            color:#047857;
            font-size:13px;
            font-weight:800;
        ">
            ✅ Resume Uploaded Successfully
        </div>

        <div style="
            color:#065f46;
            font-size:12px;
            margin-top:3px;
        ">
            📄 {uploaded_file.name}
        </div>

    </div>
    """)


    # -----------------------------------------------------
    # EXTRACT TEXT
    # -----------------------------------------------------

    text = extract_text(
        file_path
    )


    st.session_state.resume_text = text


    # -----------------------------------------------------
    # RESUME PREVIEW
    # -----------------------------------------------------

    html("""
    <div class="section-card">

        <div class="section-title">
            📄 Resume Preview
        </div>

    </div>
    """)


    st.text_area(
        "Extracted Resume Text",
        text,
        height=230,
        label_visibility="collapsed"
    )


    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    st.markdown("")


    if st.button(
        "🤖 Analyze Resume with AI",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 AI is analyzing your resume..."
        ):

            try:

                result = analyze_resume(
                    text
                )

            except Exception as e:

                if "429" in str(e):

                    st.error(
                        "⚠️ Gemini API quota exceeded. "
                        "Please try again later or use another API key."
                    )

                else:

                    st.error(
                        f"⚠️ Unable to analyze resume: {e}"
                    )

                st.stop()


        # Save result
        st.session_state.resume_analysis = result


        st.success(
            "✅ Resume Analysis Completed Successfully!"
        )


        # =================================================
        # SCORE SECTION
        # =================================================

        st.markdown(
            "### 📊 Resume Performance"
        )


        score1, score2 = st.columns(
            2
        )


        with score1:

            html(f"""
            <div class="score-card">

                <div class="score-label">
                    📄 RESUME SCORE
                </div>

                <div class="score-value">
                    {result['resume_score']}/100
                </div>

                <div class="score-desc">
                    Overall resume quality
                </div>

            </div>
            """)


        with score2:

            html(f"""
            <div class="score-card">

                <div class="score-label">
                    🎯 ATS SCORE
                </div>

                <div class="score-value">
                    {result['ats_score']}/100
                </div>

                <div class="score-desc">
                    Applicant Tracking System compatibility
                </div>

            </div>
            """)


        # =================================================
        # CANDIDATE DETAILS
        # =================================================

        html("""
        <div class="section-card">

            <div class="section-title">
                👤 Candidate Profile
            </div>

        </div>
        """)


        html(f"""
        <div class="candidate-card">

            <div class="candidate-label">
                FULL NAME
            </div>

            <div class="candidate-value">
                {result['candidate_name']}
            </div>

            <div class="candidate-label">
                EMAIL
            </div>

            <div class="candidate-value">
                {result['email']}
            </div>

        </div>
        """)


        st.markdown("")


        # =================================================
        # CAREER RECOMMENDATION
        # =================================================

        html(f"""
        <div class="section-card">

            <div class="section-title">
                🚀 Recommended Career Path
            </div>

            <div style="
                background:#eef2ff;
                border:1px solid #c7d2fe;
                border-radius:12px;
                padding:15px;
                color:#3730a3;
                font-weight:700;
                font-size:14px;
            ">
                {result['career_recommendation']}
            </div>

        </div>
        """)


        # =================================================
        # SKILLS
        # =================================================

        html("""
        <div class="section-card">

            <div class="section-title">
                💻 Technical & Professional Skills
            </div>

        </div>
        """)


        skills = result.get(
            "skills",
            []
        )


        if skills:

            skill_html = ""

            for skill in skills:

                skill_html += f"""
                <span class="skill-tag">
                    {skill}
                </span>
                """


            html(
                skill_html
            )

        else:

            st.info(
                "No skills detected."
            )


        # =================================================
        # MISSING SKILLS
        # =================================================

        html("""
        <div style="
            margin-top:25px;
            margin-bottom:12px;
            color:#0f172a;
            font-size:18px;
            font-weight:800;
        ">
            ❌ Recommended Skills to Add
        </div>
        """)


        missing_skills = result.get(
            "missing_skills",
            []
        )


        if missing_skills:

            missing_html = ""


            for skill in missing_skills:

                missing_html += f"""
                <span class="missing-tag">
                    {skill}
                </span>
                """


            html(
                missing_html
            )

        else:

            st.success(
                "🎉 No major missing skills detected!"
            )


        # =================================================
        # EDUCATION
        # =================================================

        html("""
        <div class="section-card">

            <div class="section-title">
                🎓 Education
            </div>

        </div>
        """)


        education = result.get(
            "education",
            []
        )


        if education:

            for edu in education:

                st.write(
                    "🎓",
                    edu
                )

        else:

            st.info(
                "No education details detected."
            )


        # =================================================
        # PROJECTS
        # =================================================

        html("""
        <div class="section-card">

            <div class="section-title">
                🚀 Projects
            </div>

        </div>
        """)


        projects = result.get(
            "projects",
            []
        )


        if projects:

            for project in projects:

                st.write(
                    "•",
                    project
                )

        else:

            st.info(
                "No projects detected."
            )


        # =================================================
        # STRENGTHS & WEAKNESSES
        # =================================================

        st.markdown(
            "### 💪 Profile Assessment"
        )


        strength_col, weakness_col = st.columns(
            2
        )


        with strength_col:

            html("""
            <div class="section-card">

                <div class="section-title">
                    💪 Strengths
                </div>

            </div>
            """)


            strengths = result.get(
                "strengths",
                []
            )


            if strengths:

                for strength in strengths:

                    st.success(
                        f"✔️ {strength}"
                    )

            else:

                st.info(
                    "No strengths identified."
                )


        with weakness_col:

            html("""
            <div class="section-card">

                <div class="section-title">
                    ⚠️ Areas to Improve
                </div>

            </div>
            """)


            weaknesses = result.get(
                "weaknesses",
                []
            )


            if weaknesses:

                for weakness in weaknesses:

                    st.warning(
                        f"⚠️ {weakness}"
                    )

            else:

                st.info(
                    "No major weaknesses identified."
                )


        # =================================================
        # SUGGESTIONS
        # =================================================

        html("""
        <div class="section-card">

            <div class="section-title">
                💡 AI Improvement Suggestions
            </div>

        </div>
        """)


        suggestions = result.get(
            "suggestions",
            []
        )


        if suggestions:

            for suggestion in suggestions:

                st.info(
                    f"💡 {suggestion}"
                )

        else:

            st.info(
                "No additional suggestions available."
            )


        # =================================================
        # NEXT STEP
        # =================================================

        st.markdown("")


        html("""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    #0f172a,
                    #312e81
                );

            border-radius:
                18px;

            padding:
                25px;

            margin-top:
                20px;

            text-align:
                center;

            box-shadow:
                0 12px 30px rgba(15,23,42,0.15);
        ">

            <div style="
                color:#c7d2fe;
                font-size:11px;
                font-weight:800;
                letter-spacing:0.5px;
            ">
                READY FOR THE NEXT STEP?
            </div>

            <div style="
                color:white;
                font-size:21px;
                font-weight:800;
                margin-top:6px;
            ">
                🎤 Start Your AI Mock Interview
            </div>

            <div style="
                color:#cbd5e1;
                font-size:13px;
                margin-top:5px;
            ">
                Use your resume analysis to practice personalized
                interview questions.
            </div>

        </div>
        """)


        if st.button(
            "🎤 Start AI Mock Interview",
            use_container_width=True
        ):

            st.switch_page(
                "pages/interview.py"
            )


        st.balloons()


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="resume-footer">

    🤖 AI Interview Coach
    &nbsp; • &nbsp;
    Analyze. Prepare. Succeed.

</div>
""")