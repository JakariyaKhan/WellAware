
from dotenv import load_dotenv
import os
import streamlit as st
import pickle
import numpy as np
from google import genai
from google.genai import types

# -------------------------------
# 🔹 Load environment variables
# -------------------------------
load_dotenv()
GEMINI_API_KEY = "AIzaSyBaaEQm1J0N0IDARjTFXHhcKgTFh5LaPNE"
if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found in .env file")
    st.stop()

# -------------------------------
# 🔹 ML Model Utilities
# -------------------------------
@st.cache_resource
def load_model(model_name):
    """Load ML model from file"""
    try:
        return pickle.load(open(f"models/{model_name}.pkl", "rb"))
    except Exception as e:
        st.error(f"⚠️ Error loading model '{model_name}': {e}")
        st.stop()


def predict(model, input_data):
    """Make prediction and return label & probability"""
    input_array = np.asarray(input_data).reshape(1, -1)
    result = model.predict(input_array)[0]
    try:
        prob = model.predict_proba(input_array)[:, 1][0] * 100
    except:
        prob = None
    return result, prob

# -------------------------------
# 🔹 Wellness Guide AI Chat Function
# -------------------------------
def chat_with_wellness_guide(user_input):
    """Send user input to Gemini AI and return the response"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = "gemini-2.5-flash"

    system_instruction = (
        "You are Wellness Guide AI (Wellness Guidance & Health Assistant), "
        "created by TEAM ALBATROSS. "
        "You provide medical guidance, health advice, and general wellness information "
        "in a friendly and professional manner."
    )

    contents = [
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=system_instruction)]
        ),
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    ]

    response_text = ""
    for chunk in client.models.generate_content_stream(model=model, contents=contents):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
            and chunk.candidates[0].content.parts[0].text
        ):
            response_text += chunk.candidates[0].content.parts[0].text
    return response_text

# -------------------------------
# 🔹 Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Wellness Guide AI", page_icon="🧠", layout="centered")
st.markdown("<h1 style='text-align:center;color:#4B8BBE;'>🧠 Wellness Guide AI: Assistant</h1>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:grey;'>Check your disease risk or chat with Wellness Guide AI</p>",
            unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# 🔹 Sidebar: Chat Mode
# -------------------------------
chat_mode = st.sidebar.checkbox("💬 Chat with Wellness Guide AI")

if chat_mode:
    st.subheader("💬 Chat with Wellness Guide AI")
    user_message = st.text_input("You:", "")
    if st.button("Send"):
        if user_message.strip() != "":
            with st.spinner("Wellness Guide AI is thinking..."):
                response = chat_with_wellness_guide(user_message)
            st.markdown(f"**Wellness Guide AI:** {response}")
        else:
            st.warning("Please type a message to send.")
else:
    # -------------------------------
    # 🔹 Disease Prediction Expanders
    # -------------------------------
    st.subheader("🩺 Disease Predictions")

    # -------------------------------
    # Diabetes
    # -------------------------------
    with st.expander("🩺 Diabetes Prediction", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pregnancies = st.slider("Pregnancies", 0, 17, 0)
            glucose = st.slider("Glucose", 0.0, 200.0, 99.0)
            blood_pressure = st.slider("Blood Pressure", 0.0, 180.0, 72.0)
        with col2:
            skin_thickness = st.slider("Skin Thickness", 0.0, 99.0, 20.0)
            insulin = st.slider("Insulin", 0, 900, 50)
            bmi = st.slider("BMI", 0.0, 50.0, 24.9)
        with col3:
            dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
            age = st.slider("Age", 10, 100, 25)

        model = load_model("diabetes")
        input_data = (pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age)

        if st.button("🔍 Predict Diabetes"):
            result, prob = predict(model, input_data)
            if result == 1:
                st.markdown(f"""
                    <div style="background-color:#ffcccc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:red;">⚠️ You are likely to have Diabetes</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color:#ccffcc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:green;">🎉 You are not likely to have Diabetes</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)

    # -------------------------------
    # Heart Disease
    # -------------------------------
    with st.expander("❤️ Heart Disease Prediction"):
        age = st.slider("Age", 20, 100, 40)
        sex = st.selectbox("Sex", ("Male", "Female"))
        cp = st.slider("Chest Pain Type (0-3)", 0, 3, 1)
        trestbps = st.slider("Resting Blood Pressure", 80, 200, 120)
        chol = st.slider("Cholesterol", 100, 600, 200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", (0, 1))
        restecg = st.slider("Resting ECG (0-2)", 0, 2, 1)
        thalach = st.slider("Max Heart Rate", 70, 210, 150)
        exang = st.selectbox("Exercise Induced Angina", (0, 1))
        oldpeak = st.slider("Oldpeak", 0.0, 6.0, 1.0)
        slope = st.slider("Slope (0-2)", 0, 2, 1)
        ca = st.slider("Major Vessels (0-4)", 0, 4, 0)
        thal = st.slider("Thalassemia (0-3)", 0, 3, 1)

        model = load_model("heart")
        input_data = (age, 1 if sex == "Male" else 0, cp, trestbps, chol, fbs,
                      restecg, thalach, exang, oldpeak, slope, ca, thal)

        if st.button("🔍 Predict Heart Disease"):
            result, prob = predict(model, input_data)
            if result == 1:
                st.markdown(f"""
                    <div style="background-color:#ffcccc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:red;">⚠️ You are likely to have Heart Disease</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color:#ccffcc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:green;">🎉 You are not likely to have Heart Disease</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)

    # -------------------------------
    # Cancer
    # -------------------------------
    with st.expander("🧬 Cancer Prediction"):
        mean_radius = st.slider("Mean Radius", 5.0, 30.0, 14.0)
        mean_texture = st.slider("Mean Texture", 10.0, 40.0, 20.0)
        mean_perimeter = st.slider("Mean Perimeter", 50.0, 200.0, 100.0)
        mean_area = st.slider("Mean Area", 100.0, 2500.0, 500.0)
        mean_smoothness = st.slider("Mean Smoothness", 0.05, 0.2, 0.1)

        model = load_model("cancer")
        input_data = (mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness)

        if st.button("🔍 Predict Cancer"):
            result, prob = predict(model, input_data)
            if result == 1:
                st.markdown(f"""
                    <div style="background-color:#ffcccc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:red;">⚠️ You are likely to have Cancer</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color:#ccffcc;padding:20px;border-radius:10px;text-align:center">
                        <h2 style="color:green;">🎉 You are not likely to have Cancer</h2>
                        <p style="color:black;">Probability: {prob:.2f}%</p>
                    </div>
                """, unsafe_allow_html=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:grey;font-size:12px;'>EAM ALBATROSS</p>",
            unsafe_allow_html=True)