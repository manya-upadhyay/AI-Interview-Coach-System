import streamlit as st
from database.database import create_table


# =========================================================
# DATABASE
# =========================================================

create_table()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
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

/* ==============================
   GLOBAL
   ============================== */

.stApp {
    background: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ==============================
   SIDEBAR
   ============================== */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 55%,
            #1e1b4b 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.08);
}


[data-testid="stSidebar"] * {
    color: white;
}


/* Sidebar navigation */

[data-testid="stSidebarNav"] {
    padding-top: 12px;
}


[data-testid="stSidebarNav"] a {

    border-radius: 12px;

    margin:
        5px 8px;

    padding:
        10px 14px;

    transition:
        all 0.25s ease;
}


[data-testid="stSidebarNav"] a:hover {

    background:
        rgba(255,255,255,0.10);

    transform:
        translateX(3px);
}


[data-testid="stSidebarNav"] a[aria-current="page"] {

    background:
        linear-gradient(
            90deg,
            rgba(99,102,241,0.45),
            rgba(59,130,246,0.25)
        );

    font-weight:
        700;
}


[data-testid="stSidebar"] hr {

    border-color:
        rgba(255,255,255,0.12);
}


/* ==============================
   BUTTONS
   ============================== */

.stButton > button {

    width:
        100%;

    min-height:
        48px;

    border:
        none;

    border-radius:
        12px;

    font-size:
        15px;

    font-weight:
        700;

    color:
        white;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #2563eb
        );

    box-shadow:
        0 8px 20px rgba(37,99,235,0.18);

    transition:
        all 0.25s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 28px rgba(37,99,235,0.30);
}


/* ==============================
   HERO
   ============================== */

.hero {

    position:
        relative;

    overflow:
        hidden;

    background:

        radial-gradient(
            circle at 85% 15%,
            rgba(129,140,248,0.35),
            transparent 30%
        ),

        radial-gradient(
            circle at 15% 85%,
            rgba(59,130,246,0.20),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 50%,
            #312e81 100%
        );

    padding:
        55px 50px;

    border-radius:
        26px;

    color:
        white;

    margin-bottom:
        35px;

    box-shadow:
        0 25px 50px rgba(15,23,42,0.20);
}


.hero-badge {

    display:
        inline-block;

    padding:
        8px 16px;

    border-radius:
        30px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid rgba(255,255,255,0.15);

    color:
        #c7d2fe;

    font-size:
        13px;

    font-weight:
        700;

    letter-spacing:
        0.4px;

    margin-bottom:
        18px;
}


.hero h1 {

    font-size:
        46px;

    line-height:
        1.15;

    font-weight:
        800;

    margin:
        0 0 15px 0;

    color:
        white;
}


.hero h1 span {

    background:
        linear-gradient(
            90deg,
            #a5b4fc,
            #60a5fa
        );

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;
}


.hero p {

    color:
        #cbd5e1;

    font-size:
        17px;

    line-height:
        1.7;

    max-width:
        720px;

    margin:
        0;
}


/* ==============================
   SECTION TITLE
   ============================== */

.section-title {

    font-size:
        25px;

    font-weight:
        800;

    color:
        #0f172a;

    margin:
        35px 0 18px 0;
}


/* ==============================
   STATS
   ============================== */

.stat-card {

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

    transition:
        all 0.25s ease;
}


.stat-card:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 15px 35px rgba(15,23,42,0.10);
}


.stat-icon {

    font-size:
        28px;

    margin-bottom:
        8px;
}


.stat-title {

    color:
        #64748b;

    font-size:
        13px;

    font-weight:
        600;
}


.stat-value {

    color:
        #0f172a;

    font-size:
        24px;

    font-weight:
        800;

    margin-top:
        5px;
}


/* ==============================
   FEATURE CARDS
   ============================== */

.feature-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        20px;

    padding:
        27px;

    min-height:
        215px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    transition:
        all 0.25s ease;

    margin-bottom:
        18px;
}


.feature-card:hover {

    transform:
        translateY(-5px);

    box-shadow:
        0 18px 35px rgba(15,23,42,0.10);

    border-color:
        #c7d2fe;
}


.feature-icon {

    width:
        55px;

    height:
        55px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        15px;

    background:
        #eef2ff;

    font-size:
        26px;

    margin-bottom:
        17px;
}


.feature-card h3 {

    color:
        #0f172a;

    font-size:
        18px;

    font-weight:
        750;

    margin:
        0 0 9px 0;
}


.feature-card p {

    color:
        #64748b;

    font-size:
        14px;

    line-height:
        1.65;

    margin:
        0;
}


/* ==============================
   CTA
   ============================== */

.cta {

    background:

        radial-gradient(
            circle at 90% 10%,
            rgba(129,140,248,0.30),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #111827,
            #1e1b4b
        );

    padding:
        35px;

    border-radius:
        22px;

    color:
        white;

    margin:
        35px 0;

    box-shadow:
        0 18px 40px rgba(15,23,42,0.16);
}


.cta h2 {

    color:
        white;

    font-size:
        26px;

    margin:
        0 0 8px 0;
}


.cta p {

    color:
        #cbd5e1;

    font-size:
        14px;

    line-height:
        1.6;

    margin:
        0;
}


/* ==============================
   FOOTER
   ============================== */

.footer {

    text-align:
        center;

    padding:
        25px 10px;

    margin-top:
        45px;

    border-top:
        1px solid #e2e8f0;

    color:
        #94a3b8;

    font-size:
        12px;
}


/* ==============================
   STREAMLIT CLEANUP
   ============================== */

#MainMenu {
    visibility:
        hidden;
}

footer {
    visibility:
        hidden;
}

</style>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    html("""
    <div style="
        padding: 12px 5px 18px 5px;
    ">

        <div style="
            font-size: 30px;
            margin-bottom: 8px;
        ">
            🤖
        </div>

        <div style="
            color: white;
            font-size: 20px;
            font-weight: 800;
        ">
            AI Interview Coach
        </div>

        <div style="
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.6;
            margin-top: 6px;
        ">
            Your intelligent interview<br>
            preparation partner.
        </div>

    </div>
    """)

    st.divider()

    html("""
    <div style="
        font-size: 16px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    ">
        👤 Profile
    </div>
    """)

    if "user" in st.session_state:

        html(f"""
        <div style="
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 13px;
            border-radius: 12px;
            margin-bottom: 8px;
        ">

            <div style="
                color: #94a3b8;
                font-size: 11px;
            ">
                LOGGED IN AS
            </div>

            <div style="
                color: white;
                font-size: 14px;
                font-weight: 700;
                margin-top: 4px;
            ">
                {st.session_state.user}
            </div>

        </div>
        """)

    if "email" in st.session_state:

        html(f"""
        <div style="
            color: #94a3b8;
            font-size: 12px;
            padding-left: 5px;
        ">
            ✉️ {st.session_state.email}
        </div>
        """)

    html("""
    <div style="
        color: #64748b;
        font-size: 11px;
        text-align: center;
        line-height: 1.6;
        margin-top: 35px;
    ">
        🚀 AI POWERED<br>
        INTERVIEW PREPARATION
    </div>
    """)


# =========================================================
# HERO SECTION
# =========================================================

html("""
<div class="hero">

    <div class="hero-badge">
        ✨ NEXT-GENERATION INTERVIEW PREPARATION
    </div>

    <h1>
        AI Interview <span>Coach</span>
    </h1>

    <p>
        Prepare for your next interview with an intelligent AI coach.
        Analyze your resume, practice personalized questions,
        improve your confidence and receive detailed performance feedback.
    </p>

</div>
""")


# =========================================================
# QUICK STATS
# =========================================================

html("""
<div class="section-title">
    Everything You Need to Prepare
</div>
""")


s1, s2, s3, s4 = st.columns(4)


with s1:

    html("""
    <div class="stat-card">

        <div class="stat-icon">
            📄
        </div>

        <div class="stat-title">
            RESUME
        </div>

        <div class="stat-value">
            AI Analysis
        </div>

    </div>
    """)


with s2:

    html("""
    <div class="stat-card">

        <div class="stat-icon">
            🤖
        </div>

        <div class="stat-title">
            QUESTIONS
        </div>

        <div class="stat-value">
            AI Generated
        </div>

    </div>
    """)


with s3:

    html("""
    <div class="stat-card">

        <div class="stat-icon">
            🎤
        </div>

        <div class="stat-title">
            INTERVIEW
        </div>

        <div class="stat-value">
            Voice Based
        </div>

    </div>
    """)


with s4:

    html("""
    <div class="stat-card">

        <div class="stat-icon">
            📊
        </div>

        <div class="stat-title">
            FEEDBACK
        </div>

        <div class="stat-value">
            AI Powered
        </div>

    </div>
    """)


# =========================================================
# START PRACTICING
# =========================================================

html("""
<div class="section-title">
    Start Practicing
</div>
""")


html("""
<div class="cta">

    <h2>
        🚀 Ready for your next interview?
    </h2>

    <p>
        Take an AI-powered mock interview with personalized questions,
        voice-based interaction and intelligent performance analysis.
    </p>

</div>
""")


b1, b2 = st.columns(2)


with b1:

    if st.button(
        "🎤  Start Interview",
        use_container_width=True
    ):

        st.switch_page(
            "pages/interview.py"
        )


with b2:

    if st.button(
        "📄  Analyze Resume",
        use_container_width=True
    ):

        st.switch_page(
            "pages/resume_upload.py"
        )


# =========================================================
# FEATURES
# =========================================================

html("""
<div class="section-title">
    Powerful AI Interview Features
</div>
""")


f1, f2, f3 = st.columns(3)


with f1:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            📄
        </div>

        <h3>
            Resume Analysis
        </h3>

        <p>
            Analyze your resume using AI and identify
            important skills, strengths, weaknesses and
            areas for improvement.
        </p>

    </div>
    """)


with f2:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            🤖
        </div>

        <h3>
            AI Generated Questions
        </h3>

        <p>
            Receive personalized technical and behavioral
            interview questions based on your resume and
            selected interview type.
        </p>

    </div>
    """)


with f3:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            🎤
        </div>

        <h3>
            Voice-Based Interview
        </h3>

        <p>
            Practice answering interview questions naturally
            using voice interaction and speech recognition.
        </p>

    </div>
    """)


f4, f5, f6 = st.columns(3)


with f4:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            😊
        </div>

        <h3>
            Confidence Analysis
        </h3>

        <p>
            Analyze facial expressions and confidence
            indicators during your interview session.
        </p>

    </div>
    """)


with f5:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            📊
        </div>

        <h3>
            Performance Report
        </h3>

        <p>
            Get structured AI feedback including scores,
            strengths and personalized improvement suggestions.
        </p>

    </div>
    """)


with f6:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            📥
        </div>

        <h3>
            PDF Report
        </h3>

        <p>
            Download your complete interview performance
            report and use it to track your preparation.
        </p>

    </div>
    """)


# =========================================================
# HOW IT WORKS
# =========================================================

html("""
<div class="section-title">
    How It Works
</div>
""")


h1, h2, h3 = st.columns(3)


with h1:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            1️⃣
        </div>

        <h3>
            Upload Resume
        </h3>

        <p>
            Upload your resume and let AI understand
            your skills, experience and profile.
        </p>

    </div>
    """)


with h2:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            2️⃣
        </div>

        <h3>
            Take Interview
        </h3>

        <p>
            Answer personalized questions through
            text or voice-based interview interaction.
        </p>

    </div>
    """)


with h3:

    html("""
    <div class="feature-card">

        <div class="feature-icon">
            3️⃣
        </div>

        <h3>
            Get AI Feedback
        </h3>

        <p>
            Review your performance score, feedback,
            confidence analysis and improvement areas.
        </p>

    </div>
    """)


# =========================================================
# BOTTOM ACTIONS
# =========================================================

html("""
<div class="section-title">
    Quick Access
</div>
""")


q1, q2 = st.columns(2)


with q1:

    if st.button(
        "📜  View Interview History",
        use_container_width=True
    ):

        st.switch_page(
            "pages/history.py"
        )


with q2:

    if st.button(
        "🚪  Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="footer">

    🤖 <b>AI Interview Coach</b>
    &nbsp; • &nbsp;
    Intelligent Interview Preparation Platform

    <br><br>

    Practice smarter. Build confidence. Interview better.

</div>
""")