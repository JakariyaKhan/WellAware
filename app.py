import streamlit as st

st.set_page_config(page_title="Dr. Disease Detector", page_icon="👨‍⚕️", layout="centered")

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


# ===== Sidebar =====
st.sidebar.header("🩺 App Navigation")
mode = st.sidebar.radio("Choose Mode", ["Disease Prediction", "Chatbot (Coming Soon)"])

# ===== Main Section =====
if mode == "Disease Prediction":
    st.subheader("🩺 Disease Predictions")

    with st.expander("🩸 Diabetes Prediction", expanded=True):
        st.write("👉 Input sliders will appear here...")

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

