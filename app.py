import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="CareLink AI v2.2",
    page_icon="🏥",
    layout="wide"
)

# -------------------------
# API Key Check
# -------------------------
if not api_key:
    st.error("❌ GEMINI_API_KEY not found.")
    st.stop()

# -------------------------
# Gemini Client
# -------------------------
client = genai.Client(api_key=api_key)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:

    st.title("🏥 CareLink AI v2.2")

    st.markdown("""
### Your Personal Health Companion

CareLink helps users with:

✅ Symptom Guidance

✅ Health Education

✅ Wellness Advice

✅ Rural Healthcare Support

✅ Voice Responses

✅ Fitness Coaching

⚠️ Not a substitute for professional medical care.
""")

    st.markdown("---")

    language = st.selectbox(
        "🌐 Select Language",
        ["English", "Tamil"]
    )

    mode = st.selectbox(
        "📌 Select Mode",
        [
            "Health Mentor",
            "Symptom Analysis",
            "Health Education",
            "Fitness Coach"
        ]
    )

    st.markdown("---")

    st.subheader("📊 BMI Calculator")

    height_cm = st.number_input(
        "Height (cm)",
        min_value=100,
        max_value=250,
        value=170
    )

    weight_kg = st.number_input(
        "Weight (kg)",
        min_value=20,
        max_value=300,
        value=70
    )

    if st.button("Calculate BMI"):

        bmi = weight_kg / ((height_cm / 100) ** 2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Healthy Weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        st.success(f"BMI: {bmi:.1f}")
        st.info(f"Category: {category}")

# -------------------------
# Main Header
# -------------------------
st.title("🏥 CareLink AI v2.2")

st.markdown("""
### Your Personal Health Companion

Your trusted AI health copilot for wellness, education, fitness, and everyday health guidance.
""")

# -------------------------
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Display Chat History
# -------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Chat Input
# -------------------------
user_input = st.chat_input("Ask CareLink anything...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Language Settings
    if language == "Tamil":
        language_prompt = (
            "Respond completely in Tamil using simple language."
        )
        voice_lang = "ta"
    else:
        language_prompt = (
            "Respond completely in English using simple language."
        )
        voice_lang = "en"

    # Mode Settings
    if mode == "Health Mentor":

        mode_prompt = """
You are CareLink AI.

Act as a friendly health mentor.

Help users improve:
- Sleep
- Nutrition
- Exercise
- Hydration
- Healthy habits

Do not prescribe medication.
Do not diagnose diseases.
"""

    elif mode == "Symptom Analysis":

        mode_prompt = """
You are CareLink AI.

Analyze symptoms and provide:

1. Possible causes
2. Home care suggestions
3. When to see a doctor
4. Emergency warning signs

Do not prescribe medications.
Do not provide a definitive diagnosis.
"""

    elif mode == "Health Education":

        mode_prompt = """
You are CareLink AI.

Act as a health educator.

Explain health topics clearly and simply.

Do not diagnose diseases.
"""

    else:

        mode_prompt = """
You are CareLink AI Fitness Coach.

Help users with:
- Workout routines
- Muscle gain
- Fat loss
- Strength training
- Nutrition basics
- Recovery

Provide practical fitness advice.

Do not recommend steroids.
Do not recommend dangerous dieting methods.
"""

    prompt = f"""
{mode_prompt}

{language_prompt}

User Question:
{user_input}
"""

    try:

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        ai_response = response.text

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        with st.chat_message("assistant"):

            st.markdown(ai_response)

            try:

                tts = gTTS(
                    text=ai_response[:2500],
                    lang=voice_lang
                )

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                ) as temp_audio:

                    tts.save(temp_audio.name)

                    st.audio(
                        temp_audio.name,
                        format="audio/mp3"
                    )

            except Exception:
                st.warning("Voice output unavailable.")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")

st.info(
    "⚠️ CareLink AI provides educational information only and is not a substitute for professional medical advice."
)

st.caption(
    "CareLink AI v2.2 • Built by mithilesh"
)