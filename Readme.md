# 🧠 Wellness Guide AI: Disease Prediction & Health Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5_Flash-green.svg)](https://ai.google.dev/)

A smart, interactive health assistant built with Streamlit, Gemini AI, and machine learning. This project allows users to check their risk for diabetes and chat with a friendly AI wellness guide for health tips and medical advice.

---

## 🧪 Demo Preview

> 🖥️ Displays a clean, centered dashboard with:
> - 🩺 Diabetes risk prediction using ML model
> - 💬 Chat interface with Gemini-powered Wellness Guide AI
> - 🎯 Probability-based health insights
> - 📊 Sliders for user-friendly input of health metrics

---

## 🚀 Features

- ✅ ML-based diabetes prediction using pre-trained model
- 💬 Gemini-powered AI chat for wellness guidance
- 📈 Probability score for prediction confidence
- 🧠 Friendly, professional health assistant persona
- 🧩 Modular code with clear separation of logic
- 🔐 Secure API key handling via `.env` file

---

## 🧠 How It Works

1. **Disease Prediction**:
   - User inputs health metrics via sliders.
   - ML model (loaded from `diabetes.pkl`) predicts diabetes risk.
   - Probability score is displayed with styled feedback.

2. **Wellness Chat**:
   - Gemini 2.5 Flash responds to user queries.
   - AI provides health tips, lifestyle advice, and general wellness support.

3. **Streamlit UI**:
   - Sidebar toggle for chat mode.
   - Expandable section for disease prediction.
   - Styled feedback boxes for results.

---

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- NumPy
- Pickle
- python-dotenv
- google-generativeai

### 📦 Install Dependencies

```bash
pip install streamlit numpy python-dotenv google-
```
### 📁 Project Structure
```
Wellness-Guide-AI/
├── models/
│   └── diabetes.csv           # dataset
│    └── diabetes.pkl           # Pre-trained ML model
├── .env                       # Contains GEMINI_API_KEY
├── app.py                     # Main Streamlit application
├── module.py
├── ChatWithAI.py
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```
## 👨‍💻 Author

**Jakariya Khan**  
B.Tech in Computer Science & Engineering (AI & ML)  
Passionate about real-world AI applications, computer vision, and intelligent systems.

- 📬 [LinkedIn](https://www.linkedin.com/in/jakariyakhan/)
- 🐙 [GitHub](https://github.com/JakariyaKhan)

**Shahe Aalam Ansari**  
B.Tech in Computer Science & Engineering (AI & ML)  
Passionate about real-world AI applications, computer vision, and intelligent systems.

- 📬 [LinkedIn](https://www.linkedin.com/in/shaheaalam244/)
- 🐙 [GitHub](https://github.com/shaheaalam244/)

**Arshita Mishra**                
B.Tech in Computer Science & Engineering (AI & ML)  
Passionate about real-world AI applications, computer vision, and intelligent systems.

- 📬 [LinkedIn](https://www.linkedin.com/in/arshita-mishra-4624aa333)
- 🐙 [GitHub](https://github.com/arshita291)

## 💬 Feedback & Contributions

Contributions, suggestions, and feedback are welcome!

If you find a bug, have an idea for improvement, or want to contribute to this project:
- Open an issue
- Submit a pull request
- Reach out via [LinkedIn](https://www.linkedin.com/in/jakariyakhan/)