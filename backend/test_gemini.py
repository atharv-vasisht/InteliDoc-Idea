import google.generativeai as genai
from app.core.config import settings

# Configure the API key from settings
api_key = settings.GEMINI_API_KEY
print(f"✅ Found API key: {api_key[:10]}...")

# Configure Gemini
genai.configure(api_key=api_key)

try:
    models = genai.list_models()
    print("Available models:")
    for model in models:
        print(model)
except Exception as e:
    print(f"Error listing models: {e}") 