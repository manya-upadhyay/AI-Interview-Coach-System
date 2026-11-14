import streamlit as st
from database.database import login_user


# =========================================================
# SESSION STATE
# =========================================================

st.session_state.setdefault("logged_in", False)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Login | AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
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

/* ========================================================
   PAGE
   ======================================================== */

.stApp {

    background:

        radial-gradient(
            circle at 10% 15%,
            rgba(99,102,241,0.16),
            transparent 30%
        ),

        radial-gradient(
            circle at 90% 85%,
            rgba(59,130,246,0.14),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #f8fafc,
            #eef2ff
        );
}


.block-container {

    max-width:
        1200px;

    padding-top:
        3rem;

    padding-bottom:
        3rem;
}


/* ========================================================
   HIDE STREAMLIT DEFAULT ELEMENTS
   ======================================================== */

#MainMenu {
    visibility:
        hidden;
}

footer {
    visibility:
        hidden;
}


/* ========================================================
   LEFT BRANDING
   ======================================================== */

.brand-section {

    padding:
        60px 20px 40px 20px;
}


.brand-icon {

    font-size:
        55px;

    margin-bottom:
        15px;
}


.brand-title {

    font-size:
        42px;

    font-weight:
        800;

    line-height:
        1.15;

    color:
        #0f172a;

    margin-bottom:
        15px;
}


.brand-title span {

    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #2563eb
        );

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;
}


.brand-description {

    color:
        #64748b;

    font-size:
        16px;

    line-height:
        1.7;

    max-width:
        500px;
}


/* ========================================================
   FEATURE ITEMS
   ======================================================== */

.feature-item {

    display:
        flex;

    align-items:
        center;

    gap:
        13px;

    margin-top:
        22px;

    color:
        #334155;

    font-size:
        14px;

    font-weight:
        600;
}


.feature-circle {

    width:
        35px;

    height:
        35px;

    min-width:
        35px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        #eef2ff;

    border-radius:
        10px;

    font-size:
        17px;
}


/* ========================================================
   LOGIN CARD
   ======================================================== */

.login-card {

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid #e2e8f0;

    border-radius:
        24px;

    padding:
        35px;

    box-shadow:
        0 25px 60px rgba(15,23,42,0.12);

    margin:
        15px 0;
}


.login-header {

    text-align:
        center;

    margin-bottom:
        25px;
}


.login-header-icon {

    width:
        58px;

    height:
        58px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    margin:
        0 auto 15px auto;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #2563eb
        );

    border-radius:
        16px;

    font-size:
        27px;

    box-shadow:
        0 10px 25px rgba(79,70,229,0.25);
}


.login-title {

    font-size:
        27px;

    font-weight:
        800;

    color:
        #0f172a;

    margin-bottom:
        7px;
}


.login-subtitle {

    color:
        #64748b;

    font-size:
        13px;
}


/* ========================================================
   INPUT FIELDS
   ======================================================== */

.stTextInput label {

    color:
        #334155 !important;

    font-size:
        13px !important;

    font-weight:
        600 !important;
}


.stTextInput input {

    border:
        1px solid #cbd5e1 !important;

    border-radius:
        11px !important;

    padding:
        12px 14px !important;

    background:
        #f8fafc !important;

    color:
        #0f172a !important;

    transition:
        all 0.2s ease;
}


.stTextInput input:focus {

    border:
        1px solid #6366f1 !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.10) !important;
}


/* ========================================================
   LOGIN BUTTON
   ======================================================== */

.stButton > button {

    width:
        100%;

    min-height:
        48px;

    border:
        none;

    border-radius:
        12px;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #2563eb
        );

    color:
        white;

    font-size:
        15px;

    font-weight:
        700;

    box-shadow:
        0 10px 22px rgba(37,99,235,0.20);

    transition:
        all 0.25s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 15px 30px rgba(37,99,235,0.30);
}


/* ========================================================
   INFO BOX
   ======================================================== */

.info-box {

    background:
        #f8fafc;

    border:
        1px solid #e2e8f0;

    border-radius:
        12px;

    padding:
        12px 14px;

    color:
        #64748b;

    font-size:
        12px;

    text-align:
        center;

    margin-top:
        18px;
}


/* ========================================================
   BOTTOM BRAND
   ======================================================== */

.bottom-brand {

    text-align:
        center;

    color:
        #94a3b8;

    font-size:
        11px;

    margin-top:
        20px;
}

</style>
""")


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns(
    [1.15, 0.85],
    gap="large"
)


# =========================================================
# LEFT SIDE - BRANDING
# =========================================================

with left:

    html("""
    <div class="brand-section">

        <div class="brand-icon">
            🤖
        </div>

        <div class="brand-title">
            Welcome to<br>
            <span>AI Interview Coach</span>
        </div>

        <div class="brand-description">
            Your intelligent interview preparation partner.
            Practice real-world interviews, improve your confidence
            and receive personalized AI-powered feedback.
        </div>


        <div class="feature-item">

            <div class="feature-circle">
                📄
            </div>

            AI-powered resume analysis

        </div>


        <div class="feature-item">

            <div class="feature-circle">
                🤖
            </div>

            Personalized interview questions

        </div>


        <div class="feature-item">

            <div class="feature-circle">
                🎤
            </div>

            Voice-based mock interviews

        </div>


        <div class="feature-item">

            <div class="feature-circle">
                📊
            </div>

            Detailed performance insights

        </div>


        <div class="feature-item">

            <div class="feature-circle">
                🏆
            </div>

            Build confidence for your next interview

        </div>

    </div>
    """)


# =========================================================
# RIGHT SIDE - LOGIN
# =========================================================

with right:

    html("""
    <div class="login-card">

        <div class="login-header">

            <div class="login-header-icon">
                🔐
            </div>

            <div class="login-title">
                Welcome Back
            </div>

            <div class="login-subtitle">
                Login to continue your interview preparation
            </div>

        </div>

    </div>
    """)


    # -----------------------------------------------------
    # INPUTS
    # -----------------------------------------------------

    email = st.text_input(
        "Email Address",
        placeholder="Enter your email"
    )


    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )


    # -----------------------------------------------------
    # LOGIN BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚀  Login to AI Interview Coach",
        use_container_width=True
    ):

        if not email or not password:

            st.warning(
                "⚠️ Please enter both email and password."
            )

        else:

            user = login_user(
                email,
                password
            )

            if user:

                # -----------------------------------------
                # KEEP EXISTING SESSION LOGIC
                # -----------------------------------------

                st.session_state.logged_in = True

                st.session_state.user = user[1]

                st.session_state.email = user[2]


                st.success(
                    f"Welcome {user[1]} 🎉"
                )


                st.switch_page(
                    "pages/dashboard.py"
                )


            else:

                st.error(
                    "❌ Invalid Email or Password"
                )


    # -----------------------------------------------------
    # SECURITY INFO
    # -----------------------------------------------------

    html("""
    <div class="info-box">

        🔒 Your account information is securely handled
        by the application.

    </div>


    <div class="bottom-brand">

        🤖 AI Interview Coach
        &nbsp; • &nbsp;
        Intelligent Interview Preparation

    </div>
    """)