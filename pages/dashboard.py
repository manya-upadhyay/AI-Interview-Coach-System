import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard | AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# LOGIN CHECK
# ---------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first.")
    st.stop()


user = st.session_state.get("user", "Candidate")


# ---------------------------------------------------------
# HTML HELPER
# ---------------------------------------------------------
def html(content):
    st.html(content)


# ---------------------------------------------------------
# GLOBAL UI / CSS
# ---------------------------------------------------------
html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: #f8fafc;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* ========================================================
   SIDEBAR
   ======================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #172554 55%,
        #1e1b4b 100%
    );

    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white;
}


/* Sidebar navigation */

[data-testid="stSidebarNav"] {
    padding-top: 1rem;
}

[data-testid="stSidebarNav"] a {
    border-radius: 12px;
    margin: 5px 8px;
    padding: 10px 14px;
    transition: all 0.25s ease;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.10);
    transform: translateX(3px);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(
        90deg,
        rgba(99,102,241,0.45),
        rgba(59,130,246,0.25)
    );

    font-weight: 700;
}


/* Sidebar divider */

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12);
}


/* ========================================================
   BUTTONS
   ======================================================== */

.stButton > button {
    width: 100%;
    min-height: 48px;

    border-radius: 12px;
    border: none;

    font-weight: 700;
    font-size: 15px;

    transition: all 0.25s ease;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #2563eb
    );

    color: white;

    box-shadow:
        0 8px 20px rgba(37,99,235,0.18);
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 12px 25px rgba(37,99,235,0.28);
}


/* ========================================================
   HERO
   ======================================================== */

.hero {

    background:
        radial-gradient(
            circle at top right,
            rgba(99,102,241,0.35),
            transparent 35%
        ),

        linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 55%,
            #312e81 100%
        );

    padding: 38px 42px;

    border-radius: 24px;

    color: white;

    margin-bottom: 28px;

    box-shadow:
        0 20px 45px rgba(15,23,42,0.18);
}


.hero-badge {

    display: inline-block;

    background:
        rgba(255,255,255,0.12);

    border:
        1px solid rgba(255,255,255,0.15);

    padding:
        7px 14px;

    border-radius:
        30px;

    font-size:
        13px;

    font-weight:
        600;

    margin-bottom:
        15px;
}


.hero h1 {

    font-size:
        38px;

    font-weight:
        800;

    margin:
        0 0 8px 0;
}


.hero p {

    color:
        #cbd5e1;

    font-size:
        16px;

    margin:
        0;

    max-width:
        700px;
}


/* ========================================================
   SECTION TITLE
   ======================================================== */

.section-title {

    font-size:
        23px;

    font-weight:
        800;

    color:
        #0f172a;

    margin:
        28px 0 15px 0;
}


/* ========================================================
   METRIC CARDS
   ======================================================== */

.metric-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        22px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    transition:
        all 0.25s ease;

    height:
        100%;
}


.metric-card:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 14px 30px rgba(15,23,42,0.09);
}


.metric-icon {

    font-size:
        25px;

    margin-bottom:
        10px;
}


.metric-label {

    color:
        #64748b;

    font-size:
        13px;

    font-weight:
        600;
}


.metric-value {

    color:
        #0f172a;

    font-size:
        28px;

    font-weight:
        800;

    margin-top:
        3px;
}


/* ========================================================
   FEATURE CARDS
   ======================================================== */

.feature-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        20px;

    padding:
        25px;

    min-height:
        185px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-bottom:
        12px;
}


.feature-icon {

    width:
        48px;

    height:
        48px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        #eef2ff;

    border-radius:
        14px;

    font-size:
        23px;

    margin-bottom:
        15px;
}


.feature-card h3 {

    color:
        #0f172a;

    font-size:
        18px;

    margin:
        0 0 7px 0;
}


.feature-card p {

    color:
        #64748b;

    font-size:
        14px;

    line-height:
        1.6;
}


/* ========================================================
   INTERVIEW CTA
   ======================================================== */

.interview-card {

    background:

        radial-gradient(
            circle at right top,
            rgba(129,140,248,0.25),
            transparent 35%
        ),

        linear-gradient(
            135deg,
            #111827,
            #1e1b4b
        );

    color:
        white;

    border-radius:
        22px;

    padding:
        30px;

    margin-top:
        10px;

    margin-bottom:
        25px;
}


.interview-card h2 {

    font-size:
        25px;

    margin-bottom:
        8px;
}


.interview-card p {

    color:
        #cbd5e1;

    font-size:
        14px;
}


/* ========================================================
   FOOTER
   ======================================================== */

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


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    html("""
    <div style="
        padding: 10px 4px 20px 4px;
    ">

        <div style="
            font-size: 28px;
            margin-bottom: 8px;
        ">
            🤖
        </div>

        <div style="
            font-size: 20px;
            font-weight: 800;
            color: white;
        ">
            AI Interview Coach
        </div>

        <div style="
            color: #94a3b8;
            font-size: 12px;
            margin-top: 5px;
            line-height: 1.5;
        ">
            Your intelligent interview<br>
            preparation partner.
        </div>

    </div>
    """)

    st.divider()

    html(f"""
    <div style="
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 15px;
        border-radius: 14px;
        margin-bottom: 15px;
    ">

        <div style="
            font-size: 12px;
            color: #94a3b8;
        ">
            LOGGED IN AS
        </div>

        <div style="
            font-size: 15px;
            font-weight: 700;
            color: white;
            margin-top: 4px;
        ">
            👤 {user}
        </div>

    </div>
    """)

    html("""
    <div style="
        color: #64748b;
        font-size: 11px;
        text-align: center;
        margin-top: 30px;
    ">
        AI-POWERED INTERVIEW PREPARATION<br>
        v1.0
    </div>
    """)


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
html(f"""
<div class="hero">

    <div class="hero-badge">
        ✨ AI-POWERED INTERVIEW PREPARATION
    </div>

    <h1>
        Welcome back, {user} 👋
    </h1>

    <p>
        Practice smarter, build confidence and prepare for your
        next interview with personalized AI-powered coaching.
    </p>

</div>
""")


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------
html("""
<div class="section-title">
    Your Interview Overview
</div>
""")

m1, m2, m3, m4 = st.columns(4)


with m1:

    html("""
    <div class="metric-card">

        <div class="metric-icon">
            🎯
        </div>

        <div class="metric-label">
            TOTAL INTERVIEWS
        </div>

        <div class="metric-value">
            —
        </div>

    </div>
    """)


with m2:

    html("""
    <div class="metric-card">

        <div class="metric-icon">
            📊
        </div>

        <div class="metric-label">
            AVERAGE SCORE
        </div>

        <div class="metric-value">
            —
        </div>

    </div>
    """)


with m3:

    html("""
    <div class="metric-card">

        <div class="metric-icon">
            🏆
        </div>

        <div class="metric-label">
            BEST PERFORMANCE
        </div>

        <div class="metric-value">
            —
        </div>

    </div>
    """)


with m4:

    html("""
    <div class="metric-card">

        <div class="metric-icon">
            📈
        </div>

        <div class="metric-label">
            IMPROVEMENT
        </div>

        <div class="metric-value">
            —
        </div>

    </div>
    """)


# ---------------------------------------------------------
# START PRACTICING
# ---------------------------------------------------------
html("""
<div class="section-title">
    Start Practicing
</div>
""")


html("""
<div class="interview-card">

    <h2>
        🚀 Ready for your next interview?
    </h2>

    <p>
        Take an AI-powered mock interview with personalized
        questions, voice-based interaction and intelligent
        performance analysis.
    </p>

</div>
""")


c1, c2, c3 = st.columns([1, 1, 2])


with c1:

    if st.button(
        "🎤 Start Interview",
        use_container_width=True
    ):

        st.switch_page(
            "pages/interview.py"
        )


with c2:

    if st.button(
        "📄 Analyze Resume",
        use_container_width=True
    ):

        st.switch_page(
            "pages/resume_upload.py"
        )


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------
html("""
<div class="section-title">
    AI Interview Features
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
            skills, strengths and areas for improvement.
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
            Get personalized interview questions based
            on your resume and selected interview type.
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
            Practice answering questions naturally
            using voice interaction.
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
            indicators during your interview.
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
            Get structured AI feedback with scores,
            strengths and improvement suggestions.
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
            report for future reference.
        </p>

    </div>
    """)


# ---------------------------------------------------------
# QUICK ACCESS
# ---------------------------------------------------------
html("""
<div class="section-title">
    Quick Access
</div>
""")


q1, q2 = st.columns(2)


with q1:

    if st.button(
        "📜 View Interview History",
        use_container_width=True
    ):

        st.switch_page(
            "pages/history.py"
        )


with q2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
html("""
<div style="
    text-align: center;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    color: #94a3b8;
    font-size: 12px;
">

    🤖 AI Interview Coach
    &nbsp;•&nbsp;
    Intelligent Interview Preparation Platform

</div>
""")