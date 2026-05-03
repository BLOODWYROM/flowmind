import os
import json
from google import genai

api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello"
    )
    print("SUCCESS:", response.text)
except Exception as e:
    print("ERROR:", str(e))
