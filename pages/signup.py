import streamlit as st
from database.database import register_user


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sign Up | AI Interview Coach",
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
   PAGE BACKGROUND
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
        50px 20px 40px 20px;
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
        21px;

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
   SIGNUP CARD
   ======================================================== */

.signup-card {

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


.signup-header {

    text-align:
        center;

    margin-bottom:
        25px;
}


.signup-header-icon {

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


.signup-title {

    font-size:
        27px;

    font-weight:
        800;

    color:
        #0f172a;

    margin-bottom:
        7px;
}


.signup-subtitle {

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
   REGISTER BUTTON
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
   SECURITY BOX
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
   FOOTER BRAND
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

            Start Your Journey With<br>

            <span>AI Interview Coach</span>

        </div>

        <div class="brand-description">

            Create your account and start preparing for
            interviews with an intelligent AI-powered
            interview coach designed to help you perform better.

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
                😊
            </div>

            Confidence and facial analysis

        </div>


        <div class="feature-item">

            <div class="feature-circle">
                📊
            </div>

            Detailed AI performance reports

        </div>

    </div>
    """)


# =========================================================
# RIGHT SIDE - SIGNUP
# =========================================================

with right:

    html("""
    <div class="signup-card">

        <div class="signup-header">

            <div class="signup-header-icon">
                ✨
            </div>

            <div class="signup-title">
                Create Your Account
            </div>

            <div class="signup-subtitle">
                Join AI Interview Coach and start practicing smarter
            </div>

        </div>

    </div>
    """)


    # -----------------------------------------------------
    # INPUT FIELDS
    # -----------------------------------------------------

    name = st.text_input(
        "Full Name",
        placeholder="Enter your full name"
    )


    email = st.text_input(
        "Email Address",
        placeholder="Enter your email"
    )


    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )


    # -----------------------------------------------------
    # REGISTER BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚀  Create Account",
        use_container_width=True
    ):

        if not name or not email or not password:

            st.warning(
                "⚠️ Please fill in all the fields."
            )

        else:

            if register_user(
                name,
                email,
                password
            ):

                st.success(
                    "🎉 Registration Successful! "
                    "Your account has been created."
                )

                st.info(
                    "You can now login using your email and password."
                )

            else:

                st.error(
                    "❌ Email already exists!"
                )


    # -----------------------------------------------------
    # SECURITY MESSAGE
    # -----------------------------------------------------

    html("""
    <div class="info-box">

        🔒 Your account information is securely handled
        by the application.

    </div>


    <div class="bottom-brand">

        🤖 <b>AI Interview Coach</b>
        &nbsp; • &nbsp;
        Intelligent Interview Preparation

    </div>
    """)