import streamlit as st
import pandas as pd
import json
import re

from database.database import get_interview_history


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Interview History | AI Interview Coach",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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

    border-right:
        1px solid rgba(255,255,255,0.08);
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

.history-header {

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

    padding:
        32px 35px;

    border-radius:
        23px;

    margin-bottom:
        25px;

    box-shadow:
        0 18px 40px rgba(15,23,42,0.18);
}


.history-badge {

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


.history-header h1 {

    color:
        white;

    font-size:
        36px;

    font-weight:
        800;

    margin:
        0 0 8px 0;
}


.history-header p {

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
   SECTION HEADING
   ========================================================= */

.section-heading {

    color:
        #0f172a;

    font-size:
        22px;

    font-weight:
        800;

    margin:
        22px 0 14px 0;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-card {

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        20px;

    min-height:
        115px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);

    transition:
        all 0.2s ease;
}


.metric-card:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 14px 30px rgba(15,23,42,0.09);
}


.metric-icon {

    font-size:
        20px;

    margin-bottom:
        7px;
}


.metric-label {

    color:
        #64748b;

    font-size:
        12px;

    font-weight:
        700;

    letter-spacing:
        0.3px;
}


.metric-value {

    color:
        #0f172a;

    font-size:
        27px;

    font-weight:
        800;

    margin-top:
        5px;
}


/* =========================================================
   PERFORMANCE CARD
   ========================================================= */

.performance-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        20px;

    padding:
        24px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);

    margin-top:
        18px;
}


/* =========================================================
   INTERVIEW HISTORY CARD
   ========================================================= */

.interview-card {

    background:
        white;

    border:
        1px solid #e2e8f0;

    border-radius:
        18px;

    padding:
        20px 22px;

    margin:
        13px 0;

    box-shadow:
        0 7px 22px rgba(15,23,42,0.05);

    transition:
        all 0.2s ease;
}


.interview-card:hover {

    border-color:
        #c7d2fe;

    box-shadow:
        0 12px 28px rgba(79,70,229,0.09);
}


.interview-number {

    color:
        #6366f1;

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        0.6px;

    margin-bottom:
        5px;
}


.interview-date {

    color:
        #64748b;

    font-size:
        13px;
}


.score-badge {

    display:
        inline-block;

    padding:
        8px 13px;

    border-radius:
        10px;

    font-size:
        14px;

    font-weight:
        800;

    text-align:
        center;
}


/* =========================================================
   EMPTY STATE
   ========================================================= */

.empty-card {

    background:
        white;

    border:
        1px dashed #cbd5e1;

    border-radius:
        20px;

    padding:
        45px 25px;

    text-align:
        center;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.04);
}


.empty-icon {

    font-size:
        45px;

    margin-bottom:
        10px;
}


.empty-title {

    color:
        #0f172a;

    font-size:
        21px;

    font-weight:
        800;

    margin-bottom:
        5px;
}


.empty-text {

    color:
        #64748b;

    font-size:
        14px;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    min-height:
        44px;

    border-radius:
        11px;

    font-size:
        13px;

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
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {

    border:
        1px solid #e2e8f0;

    border-radius:
        13px;

    background:
        #f8fafc;
}


/* =========================================================
   FOOTER
   ========================================================= */

.history-footer {

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
# PAGE HEADER
# =========================================================

html("""
<div class="history-header">

    <div class="history-badge">
        📊 PERFORMANCE ANALYTICS
    </div>

    <h1>
        📜 Interview History
    </h1>

    <p>
        Track your interview performance, review previous attempts
        and monitor your progress over time.
    </p>

</div>
""")


# =========================================================
# GET HISTORY
# =========================================================

history = get_interview_history(
    st.session_state.email
)


# =========================================================
# EMPTY HISTORY
# =========================================================

if not history:

    html("""
    <div class="empty-card">

        <div class="empty-icon">
            📭
        </div>

        <div class="empty-title">
            No Interview History Yet
        </div>

        <div class="empty-text">
            Complete your first AI mock interview and
            your performance will appear here.
        </div>

    </div>
    """)

    st.stop()


# =========================================================
# SCORE PARSING
# =========================================================

scores = []

for interview in history:

    try:

        scores.append(
            float(interview[1])
        )

    except:

        pass


# =========================================================
# SAFE METRICS
# =========================================================

completed = len(scores)

total_interviews = len(history)

if scores:

    average_score = (
        sum(scores) / len(scores)
    )

    best_score = max(scores)

else:

    average_score = 0

    best_score = 0


# =========================================================
# METRIC CARDS
# =========================================================

html("""
<div class="section-heading">
    📌 Your Interview Overview
</div>
""")


col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)


with col1:

    html(f"""
    <div class="metric-card">

        <div class="metric-icon">
            📄
        </div>

        <div class="metric-label">
            TOTAL INTERVIEWS
        </div>

        <div class="metric-value">
            {total_interviews}
        </div>

    </div>
    """)


with col2:

    html(f"""
    <div class="metric-card">

        <div class="metric-icon">
            ⭐
        </div>

        <div class="metric-label">
            AVERAGE SCORE
        </div>

        <div class="metric-value">
            {average_score:.1f}
        </div>

    </div>
    """)


with col3:

    html(f"""
    <div class="metric-card">

        <div class="metric-icon">
            🏆
        </div>

        <div class="metric-label">
            BEST SCORE
        </div>

        <div class="metric-value">
            {best_score:.1f}
        </div>

    </div>
    """)


with col4:

    html(f"""
    <div class="metric-card">

        <div class="metric-icon">
            ✅
        </div>

        <div class="metric-label">
            COMPLETED
        </div>

        <div class="metric-value">
            {completed}
        </div>

    </div>
    """)


# =========================================================
# PERFORMANCE TREND
# =========================================================

html("""
<div class="section-heading">
    📈 Performance Trend
</div>
""")


if scores:

    chart_data = pd.DataFrame({
        "Interview": range(
            1,
            len(scores) + 1
        ),

        "Score": scores
    })


    html("""
    <div class="performance-card">

        <div style="
            color:#0f172a;
            font-size:16px;
            font-weight:800;
            margin-bottom:5px;
        ">
            📊 Score Progress
        </div>

        <div style="
            color:#64748b;
            font-size:13px;
            margin-bottom:15px;
        ">
            Your performance across completed interviews.
        </div>

    </div>
    """)


    st.line_chart(
        chart_data.set_index(
            "Interview"
        ),
        use_container_width=True
    )


# =========================================================
# HISTORY LIST
# =========================================================

html("""
<div class="section-heading">
    🗂️ Previous Interviews
</div>
""")


for idx, interview in enumerate(
    history
):

    date = interview[0]

    raw_score = interview[1]

    report_data = interview[2]


    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    try:

        score = float(
            raw_score
        )

    except:

        score = 0


    # -----------------------------------------------------
    # SCORE STATUS
    # -----------------------------------------------------

    if score >= 80:

        badge_bg = "#dcfce7"

        badge_color = "#166534"

        status = "Excellent"


    elif score >= 60:

        badge_bg = "#fef3c7"

        badge_color = "#92400e"

        status = "Good"


    else:

        badge_bg = "#fee2e2"

        badge_color = "#991b1b"

        status = "Needs Improvement"


    # -----------------------------------------------------
    # INTERVIEW CARD
    # -----------------------------------------------------

    c1, c2 = st.columns(
        [4, 1]
    )


    with c1:

        html(f"""
        <div class="interview-card">

            <div class="interview-number">
                INTERVIEW #{idx + 1}
            </div>

            <div style="
                color:#0f172a;
                font-size:17px;
                font-weight:800;
                margin-bottom:5px;
            ">
                🎤 AI Mock Interview
            </div>

            <div class="interview-date">
                📅 {date}
            </div>

        </div>
        """)


    with c2:

        html(f"""
        <div style="
            background:{badge_bg};
            border-radius:13px;
            padding:14px 10px;
            text-align:center;
            margin-top:13px;
        ">

            <div style="
                color:{badge_color};
                font-size:11px;
                font-weight:700;
            ">
                {status.upper()}
            </div>

            <div style="
                color:{badge_color};
                font-size:23px;
                font-weight:800;
                margin-top:3px;
            ">
                {score:.1f}
            </div>

            <div style="
                color:{badge_color};
                font-size:10px;
            ">
                / 100
            </div>

        </div>
        """)


    # -----------------------------------------------------
    # REPORT EXPANDER
    # -----------------------------------------------------

    with st.expander(
        f"📋  View Interview #{idx + 1} Report"
    ):

        html("""
        <div style="
            color:#0f172a;
            font-size:15px;
            font-weight:800;
            margin-bottom:12px;
        ">
            📊 Interview Performance Report
        </div>
        """)


        # Try to parse JSON report
        report_json = None


        try:

            report_json = json.loads(
                report_data
            )

        except:

            report_json = None


        if isinstance(
            report_json,
            dict
        ):

            # ---------------------------------------------
            # REPORT METRICS
            # ---------------------------------------------

            r1, r2, r3, r4 = st.columns(
                4
            )


            with r1:

                st.metric(
                    "⭐ Overall",
                    f"{report_json.get('overall_score', score)}/100"
                )


            with r2:

                st.metric(
                    "💻 Technical",
                    f"{report_json.get('technical', 0)}/10"
                )


            with r3:

                st.metric(
                    "🧠 Problem Solving",
                    f"{report_json.get('problem_solving', 0)}/10"
                )


            with r4:

                st.metric(
                    "🗣 Communication",
                    f"{report_json.get('communication', 0)}/10"
                )


            # ---------------------------------------------
            # STRENGTHS
            # ---------------------------------------------

            strengths = report_json.get(
                "strengths",
                []
            )


            if strengths:

                st.markdown(
                    "### ✅ Strengths"
                )


                if isinstance(
                    strengths,
                    list
                ):

                    for item in strengths:

                        st.success(
                            f"✔️ {item}"
                        )

                else:

                    st.write(
                        strengths
                    )


            # ---------------------------------------------
            # WEAKNESSES
            # ---------------------------------------------

            weaknesses = report_json.get(
                "weaknesses",
                []
            )


            if weaknesses:

                st.markdown(
                    "### ⚠️ Areas for Improvement"
                )


                if isinstance(
                    weaknesses,
                    list
                ):

                    for item in weaknesses:

                        st.warning(
                            f"⚠️ {item}"
                        )

                else:

                    st.write(
                        weaknesses
                    )


            # ---------------------------------------------
            # SUGGESTIONS
            # ---------------------------------------------

            suggestions = report_json.get(
                "suggestions",
                []
            )


            if suggestions:

                st.markdown(
                    "### 💡 Suggestions"
                )


                if isinstance(
                    suggestions,
                    list
                ):

                    for item in suggestions:

                        st.info(
                            f"💡 {item}"
                        )

                else:

                    st.write(
                        suggestions
                    )


            # ---------------------------------------------
            # FINAL RECOMMENDATION
            # ---------------------------------------------

            recommendation = report_json.get(
                "final_recommendation",
                ""
            )


            if recommendation:

                st.markdown(
                    "### 🎯 Final Recommendation"
                )

                st.success(
                    recommendation
                )


        else:

            # ---------------------------------------------
            # FALLBACK FOR OLD REPORT FORMAT
            # ---------------------------------------------

            st.markdown(
                report_data
            )


        # ---------------------------------------------
        # PDF DOWNLOAD
        # ---------------------------------------------

        st.markdown("---")


        try:

            from utils.pdf_generator import generate_pdf


            hist_pdf_path = generate_pdf(
                report_data
            )


            with open(
                hist_pdf_path,
                "rb"
            ) as pdf_file:

                pdf_bytes = pdf_file.read()


            st.download_button(
                "📄  Download This Interview Report",
                data=pdf_bytes,
                file_name=f"Interview_Report_{idx + 1}.pdf",
                mime="application/pdf",
                key=f"hist_pdf_{idx}",
                use_container_width=True
            )


        except Exception as e:

            print(
                "History PDF error:",
                e
            )


# =========================================================
# FOOTER
# =========================================================

html("""
<div class="history-footer">

    🤖 AI Interview Coach
    &nbsp; • &nbsp;
    Track. Practice. Improve.

</div>
""")