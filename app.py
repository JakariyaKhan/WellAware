import streamlit as st
import pickle
import numpy as np
import pyttsx3
from google import genai
from google.genai import types

# ===== Load Environment =====
GEMINI_API_KEY = "AIzaSyBaaEQm1J0N0IDARjTFXHhcKgTFh5LaPNE"
if not GEMINI_API_KEY:
    st.error("⚠ GEMINI_API_KEY not found in .env file")
    st.stop()

# ===== Streamlit Page Config =====
st.set_page_config(page_title="WellAware AI", page_icon="👨‍⚕", layout="centered")

# ===== Custom CSS =====
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
    font-family: "Helvetica Neue", sans-serif;
}

/* === Increase Full App Content Width === */
main.block-container {
    max-width: 1400px !important;
    padding-left: 50px !important;
    padding-right: 50px !important;
}

/* === Expand Disease Section (Expander) Width === */
div[data-testid="stExpander"] {
    max-width: 1400px !important;
    width: 100% !important;
    margin: 0 auto !important;
}

/* Improve column spacing */
.stColumn {
    padding: 0 10px !important;
}

/* Fix text color inside sliders etc. */
h1,h2,h3,label,p,span,.stMarkdown { color:#ffffff !important; }

[data-testid="stHeader"] {
    max-width: 1400px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

h1, h2, h3 {
    text-align: center !important;
    white-space: nowrap !important;
    font-weight: 700 !important;
}

div.stButton > button {
    background-color:#4B8BBE !important;
    color:white !important;
    font-weight:700 !important;
    border-radius:10px !important;
    border:none;
    transition:0.3s;
    height:3em;
}
div.stButton > button:hover {
    background-color:#3a73a0 !important;
    transform:scale(1.03);
}

.result-box {
    background-color: rgba(30,30,30,0.85);
    border-radius:12px;
    padding:20px;
    text-align:center;
    box-shadow:0px 3px 10px rgba(0,0,0,0.5);
    margin-top:10px;
    color:white;
}
.positive {background-color:#ff4d4d; color:white;}
.negative {background-color:#33cc33; color:white;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown("<h1 style='text-align:center;color:#4B8BBE; font-size:48px'>WellAware AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:grey; font-size:20px'>A Smart Healthcare Solution Integrating Machine Learning and AI-Driven Chat Interaction</p>", unsafe_allow_html=True)
st.markdown("---")

# ===== Cached Model Loader =====
@st.cache_resource
def load_model(model_name):
    try:
        model_data = pickle.load(open(f"models/{model_name}.pkl", "rb"))
        if isinstance(model_data, dict):
            return model_data.get("model"), model_data.get("scaler"), model_data.get("accuracy"), model_data.get("f1")
        return model_data, None, None, None
    except Exception as e:
        st.error(f"❌ Error loading model '{model_name}': {e}")
        st.stop()

# ===== Prediction Function =====
def predict(model, input_data, scaler=None):
    input_array = np.array(input_data).reshape(1, -1)
    if scaler:
        input_array = scaler.transform(input_array)
    result = model.predict(input_array)[0]
    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(input_array)[0][1] * 100
    return result, prob

# ===== AI Chat Function =====
def chat_with_ai_doctor(user_input):
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_instruction = (
        "You are AI Doctor, created by Team ALBATROSS. "
        "Provide medical advice only based on standard medical guidelines. "
        "Refuse non-medical questions politely. "
        "Keep responses short, clear, and professional in English or Hinglish. "
        "Always remind users to consult a real doctor for confirmation."
    )

    contents = [
        types.Content(role="model", parts=[types.Part(text=system_instruction)]),
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    response_text = ""
    for chunk in client.models.generate_content_stream(model="gemini-2.5-flash", contents=contents):
        if chunk.candidates and chunk.candidates[0].content.parts:
            response_text += chunk.candidates[0].content.parts[0].text

    return response_text.strip()

# ===== Initialize pyttsx3 engine =====
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)
engine.setProperty('pitch', 92)

# ===== Text-to-Speech Function =====
def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"🔊 Error in speech: {e}")

# ===== Sidebar Chat Toggle =====
chat_mode = st.sidebar.checkbox("💬 Chat with AI Doctor")

# ===== Chat Section =====
if chat_mode:
    st.subheader("💬 Chat with AI Doctor")

    if "user_message" not in st.session_state:
        st.session_state.user_message = ""
    if "ai_response" not in st.session_state:
        st.session_state.ai_response = ""

    user_message = st.text_input(
        "You:",
        value="",
        placeholder="Ask your health-related question...",
        key="user_input",
        on_change=lambda: st.session_state.update(
            {"ai_response": chat_with_ai_doctor(st.session_state.user_input)}
        )
    )
    col1, col2 = st.columns([0.15, 0.15])
    with col1:
        send_clicked = st.button("📨 Send Message", use_container_width=True)
    with col2:
        speak_clicked = st.button("🔊 Speak", use_container_width=True)

    if send_clicked:
        if not user_message.strip():
            st.warning("Please type your question first.")
        else:
            with st.spinner("AI Doctor is thinking..."):
                st.session_state.ai_response = chat_with_ai_doctor(user_message)
                st.session_state.user_message = user_message

    if st.session_state.ai_response:
        st.markdown("### 🧠 AI Doctor’s Response:")
        st.success(st.session_state.ai_response)
        st.info("⚕ This is general medical guidance. Please consult a real doctor for confirmation.")

        if speak_clicked:
            speak_text(st.session_state.ai_response)

# ===== Disease Prediction Section =====
else:
    st.subheader("🩺 Disease Predictions")

    # ===== Diabetes Prediction =====
    with st.expander("🩸 Diabetes Prediction", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            pregnancies = st.slider("Pregnancies", 0, 17, 0)
            glucose = st.slider("Glucose Level", 0.0, 200.0, 99.0)
            blood_pressure = st.slider("Blood Pressure", 0.0, 180.0, 72.0)
            skin_thickness = st.slider("Skin Thickness", 0.0, 99.0, 20.0)

        with col2:
            insulin = st.slider("Insulin Level", 0, 900, 50)
            bmi = st.slider("BMI (Body Mass Index)", 0.0, 50.0, 24.9)
            dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
            age = st.slider("Age", 10, 100, 25)

        if st.button("🔍 Predict Diabetes"):
            diabetes_model, _, _, _ = load_model("diabetes")
            input_data = (pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age)
            result, prob = predict(diabetes_model, input_data)
            color_class = "positive" if result == 1 else "negative"
            msg = "⚠ Likely to have Diabetes" if result == 1 else "🎉 Not likely to have Diabetes"
            st.markdown(
                f"<div class='result-box {color_class}'><h2>{msg}</h2><p>Probability: {prob:.2f}%</p></div>",
                unsafe_allow_html=True
            )
    with st.expander("❤ Heart Disease Prediction"):
        st.info("🚧 Coming Soon — This feature will be available in future updates.")

    # ===== Lung Disease Prediction =====
    with st.expander("🫁 Lung Disease Prediction"):
        st.info("🚧 Coming Soon — This feature will be available in future updates.")

    # ===== Mental Health Assessment =====
    with st.expander("🧠 Mental Health Assessment"):
        st.info("🚧 Coming Soon — This feature will be available in future updates.")

# ===== Footer =====
st.markdown("""
<p style='text-align:center;color:grey;font-size:12px;'>
⚕ This app provides AI-based medical guidance following standard medical guidelines.<br>
Always consult a qualified doctor for final diagnosis.<br><br> Team ALBATROSS </b>
</p>
""", unsafe_allow_html=True)