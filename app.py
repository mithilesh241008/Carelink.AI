```python
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="CareLink AI",
    page_icon="🏥",
    layout="wide"
)

# -------------------------
# API Key Check
# -------------------------
if not api_key:
    st.error("❌ Gemini API Key not found.")
    st.info("Please add GEMINI_API_KEY to your environment variables.")
    st.stop()

# -------------------------
# Gemini Client
# -------------------------
client = genai.Client(api_key=api_key)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.title("🏥 CareLink AI")

    st.markdown("""
    CareLink AI helps rural communities access basic healthcare guidance.

    ⚠️ **Important:** This tool is for educational purposes only and does not replace professional medical advice.
    """)

    st.markdown("---")

    st.subheader("Features")

    st.markdown("""
    ✅ Symptom Analysis

    ✅ Health Guidance

    ✅ AI Powered

    ✅ Rural Healthcare Support
    """)

# -------------------------
# Main Page
# -------------------------
st.title("🏥 CareLink AI")
st.subheader("AI-Powered Rural Healthcare Assistant")

st.markdown("---")

symptoms = st.text_area(
    "Describe your symptoms:",
    placeholder="Example: Fever, headache, sore throat for 2 days..."
)

# -------------------------
# Analyze Button
# -------------------------
if st.button("🔍 Analyze Symptoms"):

    if not symptoms.strip():
        st.warning("Please enter your symptoms.")
        st.stop()

    prompt = f"""
You are CareLink AI, a healthcare education assistant.

User symptoms:
{symptoms}

Provide:

1. Possible causes
2. Recommended home care
3. When to visit a doctor
4. Emergency warning signs

Rules:
- Keep explanations simple and easy to understand.
- Do NOT prescribe medications.
- Do NOT provide a definitive diagnosis.
- Clearly mention that this is educational information only.
"""

    try:
        with st.spinner("Analyzing symptoms..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("Analysis Complete")

        st.markdown("## 🩺 Health Guidance")
        st.write(response.text)

        st.markdown("---")

        st.info(
            "⚠️ This information is educational only and should not replace advice from a qualified healthcare professional."
        )

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")

st.caption(
    "Built by Mithilesh • Powered by Google Gemini + Streamlit"
)
```
