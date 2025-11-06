# WellAware AI
## A full Streamlit-based healthcare app integrating ML disease prediction (Diabetes, Heart), Gemini-based AI chat,
# WellAware AI

A Streamlit-based healthcare app that integrates machine learning disease prediction (Diabetes, Heart planned) with a Gemini-based AI chat assistant.

## Features
- Interactive disease prediction UI built with `streamlit`.
- Diabetes prediction using a serialized ML model (`models/diabetes.pkl`) with optional scaler.
- Prototype Gemini chat integration (server-side) using `google-genai` (chat feature marked "Coming Soon" in UI).
- Clean, responsive UI and model loading with caching.

## Repository layout
- `app.py` — Main Streamlit app (UI, model loader `load_model`, prediction `predict`, and `chat_with_ai_doctor`).
- `ChatWithAI.py` — Minimal example showing how to call Gemini via `google-genai`.
- `models/` — Directory for pickled model files (e.g., `diabetes.pkl`).
- `README.md` — This file.

## Quick start (macOS)
1. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`

2. Install dependencies:
   - `pip install streamlit numpy google-genai scikit-learn`

3. Configure the Gemini API key securely (do not hard-code in files):
   - `export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"`

4. Ensure models are available:
   - Place model pickles in `models/` (e.g., `models/diabetes.pkl`).
   - Supported pickle shape: either a plain model object or a `dict` with keys: `model`, `scaler`, `accuracy`, `f1`.

5. Run the app:
   - `streamlit run app.py`

## How predictions work
- `load_model(model_name)`: loads `models/{model_name}.pkl`. If a dict is stored, it returns `(model, scaler, accuracy, f1)`.
- `predict(model, input_data, scaler=None)`: prepares input, optionally scales it, calls `model.predict`, and returns class + probability (if `predict_proba` available).

## Gemini chat
- `ChatWithAI.py` demonstrates usage of `google-genai` with a `GEMINI_API_KEY`. For production, set the key via environment variables and remove any hard-coded keys from source files.
- In `app.py`, `chat_with_ai_doctor` streams content from the Gemini model (`gemini-2.5-flash` in the code).

## Security notes
- Never commit API keys or secrets. Use environment variables or a secrets manager.
- Remove any hard-coded API key from `ChatWithAI.py` before committing.

## Contributing
- Add models to `models/` following the expected pickle format.
- Open issues or PRs for new disease modules, UI improvements, or chat integration.

## License
- Add a license file as needed.