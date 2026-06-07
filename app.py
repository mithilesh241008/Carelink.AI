import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure page
st.set_page_config(
    page_title="CareLink AI",
    page_icon="🏥",
    layout="wide"
)

# Verify API key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env")
    st.stop()

# Gemini Client
client = genai.Client(api_key=api_key)

# Sidebar
with st.sidebar:
    st.title("🏥 CareLink AI")

    st.write("""
    CareLink AI helps rural communities receive
    basic healthcare guidance.

    ⚠️ This is not a replacement for professional medical care.
    """)

    st.markdown("---")

    st.subheader("Features")
    st.write("✅ Symptom Analysis")
    st.write("✅ Health Guidance")
    st.write("✅ AI Powered")
    st.write("✅ Rural Healthcare Support")

# Main Page
st.title("🏥 CareLink AI")
st.subheader("AI-Powered Rural Healthcare Assistant")

st.markdown("---")

symptoms = st.text_area(
    "Describe your symptoms:",
    placeholder="Example: Fever, headache, body pain for 2 days..."
)

if st.button("🔍 Analyze Symptoms"):

    if not symptoms.strip():
        st.warning("Please enter your symptoms.")
        st.stop()

    prompt = f"""
You are CareLink AI.

The user reports:

{symptoms}

Provide:

1. Possible causes
2. Home care suggestions
3. When to visit a doctor
4. Emergency warning signs

Keep explanations simple.

Do not prescribe medications.
Do not provide a definitive diagnosis.
Remind the user that this is educational information only.
"""

    try:
        with st.spinner("Analyzing..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("Analysis Complete")

        st.markdown("## 🩺 Health Guidance")
        st.write(response.text)

        st.info(
            "⚠️ This information is educational only and is not a substitute for professional medical advice."
        )

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Built by Mithilesh • Powered by Gemini + Streamlit")