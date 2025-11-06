# To run this code you need to install the following dependencies:
# pip install google-genai

#AIzaSyBaaEQm1J0N0IDARjTFXHhcKgTFh5LaPNE

# To run this code you need to install the following dependencies:
# pip install google-genai

from google import genai

def chat_with_gemini():
    # ✅ Paste your API key directly here
    GEMINI_API_KEY = "AIzaSyBaaEQm1J0N0IDARjTFXHhcKgTFh5LaPNE"

    # Initialize the client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Model name (text-only model)
    model = "gemini-2.0-flash"

    # Input message
    prompt = "Hello"

    # Send request
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    # Print response
    print(response.text)

if __name__ == "__main__":
    chat_with_gemini()
