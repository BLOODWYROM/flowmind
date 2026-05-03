import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
client = genai.Client(api_key=api_key, http_options=types.HttpOptions(api_version="v1"))

try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Say hello"
    )
    print("SUCCESS 1.5-flash v1:", response.text)
except Exception as e:
    print("ERROR:", str(e))
