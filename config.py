import os
from dotenv import load_dotenv

load_dotenv()

# Local development: read from .env.
# Streamlit Community Cloud: read from App Secrets.
try:
    import streamlit as st
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        GEMINI_API_KEY = None
except Exception:
    GEMINI_API_KEY = None

if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
