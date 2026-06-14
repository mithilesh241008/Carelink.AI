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
    page_title="CareLink AI v2.3",
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

    st.title("🏥 CareLink AI v2.3")

    st.markdown("""
### Your Personal Health Companion

CareLink helps users with:

✅ Symptom Guidance  
✅ Health Education  
✅ Wellness Advice  
✅ Rural Healthcare Support  
✅ Voice Responses  
✅ Fitness Coaching  
✅ AI Fitness Planner  

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
            "Fitness Coach",
            "Fitness Planner"
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
st.title("🏥 CareLink AI v2.3")

st.markdown("""
### Your Personal Health Companion

Your trusted AI health copilot for wellness, education, fitness, and everyday health guidance.
""")

# -------------------------
# FITNESS PLANNER
# -------------------------
if mode == "Fitness Planner":

    st.markdown("---")
    st.header("🏋️ AI Fitness Planner")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 13, 100, 18)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", 100, 250, 170)
        weight = st.number_input("Weight (kg)", 20, 300, 70)

    with col2:
        goal = st.selectbox(
            "Goal",
            ["Muscle Gain", "Fat Loss", "Body Recomposition", "Athletic Performance"]
        )

        experience = st.selectbox(
            "Experience",
            ["Beginner", "Intermediate", "Advanced"]
        )

        location = st.selectbox("Workout Location", ["Home", "Gym"])

        days = st.slider("Training Days/Week", 3, 7, 5)

    if st.button("🚀 Generate Fitness Plan"):

        prompt = f"""
You are a professional fitness coach AI.

Create a complete structured fitness plan.

User Data:
Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
Goal: {goal}
Experience: {experience}
Location: {location}
Training Days: {days}

Provide:
- Weekly workout split
- Daily workout plan
- Calories target
- Protein, carbs, fats
- Sample diet plan
- Recovery advice

Keep it simple and practical.
"""

        try:
            with st.spinner("Generating plan..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.success("Fitness Plan Ready")
            st.markdown(response.text)

            # Voice output
            try:
                tts = gTTS(text=response.text[:2500], lang="en")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts.save(f.name)
                    st.audio(f.name)

            except:
                st.warning("Voice output unavailable.")

        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# CHAT INPUT
# -------------------------
user_input = st.chat_input("Ask CareLink anything...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Language
    if language == "Tamil":
        lang_prompt = "Respond in simple Tamil."
        voice_lang = "ta"
    else:
        lang_prompt = "Respond in simple English."
        voice_lang = "en"

    # Mode prompts
    if mode == "Health Mentor":
        mode_prompt = "Act as a friendly health mentor."

    elif mode == "Symptom Analysis":
        mode_prompt = "Analyze symptoms and suggest possible causes and care."

    elif mode == "Health Education":
        mode_prompt = "Explain health topics simply."

    elif mode == "Fitness Coach":
        mode_prompt = "Act as a fitness coach giving workout advice."

    else:
        mode_prompt = "Help with fitness planning and training structure."

    final_prompt = f"""
{mode_prompt}

{lang_prompt}

User: {user_input}
"""

    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )

        answer = response.text

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

            try:
                tts = gTTS(text=answer[:2500], lang=voice_lang)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts.save(f.name)
                    st.audio(f.name)

            except:
                st.warning("Voice output unavailable.")

    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.info("⚠️ Educational purposes only. Not medical advice.")
st.caption("CareLink AI v2.3 • Built by Mithilesh ")