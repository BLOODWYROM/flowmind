from dotenv import load_dotenv
load_dotenv('.env.local')

from google import genai
from google.genai import types
import os

_api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY"))

try:
    client = genai.Client(
        api_key=_api_key,
        http_options=types.HttpOptions(api_version="v1")
    )
    print("Testing gemini-1.5-flash with v1...")
    res = client.models.generate_content(model="gemini-1.5-flash", contents="hello")
    print("v1 success:", res.text)
except Exception as e:
    print("v1 error:", e)

try:
    client_beta = genai.Client(
        api_key=_api_key
    )
    print("Testing gemini-1.5-flash with default api_version...")
    res = client_beta.models.generate_content(model="gemini-1.5-flash", contents="hello")
    print("default success:", res.text)
except Exception as e:
    print("default error:", e)

try:
    client_beta = genai.Client(
        api_key=_api_key
    )
    print("Testing gemini-2.5-flash with default api_version...")
    res = client_beta.models.generate_content(model="gemini-2.5-flash", contents="hello")
    print("default success 2.5:", res.text)
except Exception as e:
    print("default error 2.5:", e)
