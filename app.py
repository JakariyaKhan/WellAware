import streamlit as st
import numpy as np
import pickle
import os
from google import genai
from google.genai import types



st.set_page_config(page_title="Dr. Disease Detector", page_icon="👨‍⚕️", layout="centered")

@st.cache_resource
def load_model(model_name):
    try:
        data = pickle.load(open(f"models/{model_name}.pkl", "rb"))
        if isinstance(data, dict):
            return data.get("model"), data.get("scaler"), data.get("accuracy"), data.get("f1")
        return data, None, None, None
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
    font-family: "Helvetica Neue", sans-serif;
}
main.block-container {
    max-width: 1400px !important;
    padding-left: 50px !important;
    padding-right: 50px !important;
}

div[data-testid="stExpander"] {
    max-width: 1400px !important;
    width: 100% !important;
    margin: 0 auto !important;
}

h1,h2,h3,label,p,span,.stMarkdown { color:#ffffff !important; }

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
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown("<h1 style='text-align:center;color:#4B8BBE; font-size:48px'>👨‍⚕️ AI Powered Dr. Disease Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:grey; font-size:20px'>A Smart Healthcare Solution Integrating Machine Learning and AI-Driven Chat Interaction</p>", unsafe_allow_html=True)
st.markdown("---")

def predict(model, input_data, scaler=None):
    x = np.array(input_data).reshape(1, -1)
    if scaler:
        x = scaler.transform(x)
    result = model.predict(x)[0]
    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(x)[0][1] * 100
    return result, prob


def chat_with_ai_doctor(user_input):
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_prompt = (
        "You are AI Doctor, created by Shahe Aalam Ansari. "
        "Answer briefly in English or Hinglish, and always advise the user to consult a real doctor."
    )
    contents = [
        types.Content(role="system", parts=[types.Part(text=system_prompt)]),
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    response = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents
    ):
        if chunk.candidates and chunk.candidates[0].content.parts:
            response += chunk.candidates[0].content.parts[0].text
    return response.strip()

# Example run
if __name__ == "__main__":
    print(chat_with_ai_doctor("I have fever and cough, what should I do?"))

st.header("🩺 Disease Predictions")


# ===== Sidebar =====
st.sidebar.header("🩺 App Navigation")
mode = st.sidebar.radio("Choose Mode", ["Disease Prediction", "Chatbot (Coming Soon)"])

# ===== Main Section =====
if mode == "Disease Prediction":

    with st.expander("🩸 Diabetes Prediction", expanded=True):
        pregnancies = st.slider("Pregnancies", 0, 17, 0)
        glucose = st.slider("Glucose", 0.0, 200.0, 99.0)
        blood_pressure = st.slider("Blood Pressure", 0.0, 180.0, 72.0)
        skin_thickness = st.slider("Skin Thickness", 0.0, 99.0, 20.0)
        insulin = st.slider("Insulin", 0, 900, 50)
        bmi = st.slider("BMI", 0.0, 50.0, 24.9)
        dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
        age = st.slider("Age", 10, 100, 25)

        if st.button("🔍 Predict Diabetes"):
            model, _, _, _ = load_model("diabetes")
            result, prob = predict(model,
                                   [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age])
            msg = "⚠️ Likely to have Diabetes" if result == 1 else "🎉 Not likely to have Diabetes"
            st.success(f"{msg} | Probability: {prob:.2f}%")

    with st.expander("❤️ Heart Disease Prediction"):
        st.write("👉 Input sliders will appear here...")

    with st.expander("🧬 Cancer Disease Prediction"):
        st.write("👉 Coming soon...")

else:
    st.subheader("💬 Chat with AI Doctor (Coming Soon)")
    st.write("Chat system will be added later in Step 3.")

# ===== Footer =====
st.markdown("""
<p style='text-align:center;color:grey;font-size:12px;'>
⚕️ This app provides AI-based medical guidance following standard medical guidelines.<br>
Always consult a qualified doctor for final diagnosis.<br><br>
<b> TEAM Albatross❤️</b>
</p>
""", unsafe_allow_html=True)



