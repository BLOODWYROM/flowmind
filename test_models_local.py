import os
from google import genai
from google.genai import types

k = "AIzaSyDVcFTC_tCPMKKSufazC6yG7MMISkktU4o"

try:
    print("Testing gemini-1.5-flash with v1...")
    client = genai.Client(api_key=k, http_options=types.HttpOptions(api_version="v1"))
    res = client.models.generate_content(model="gemini-1.5-flash", contents="hi")
    print("v1 success:", res.text)
except Exception as e:
    print("v1 error:", e)

try:
    print("Testing gemini-1.5-flash without v1...")
    client2 = genai.Client(api_key=k)
    res = client2.models.generate_content(model="gemini-1.5-flash", contents="hi")
    print("default success:", res.text)
except Exception as e:
    print("default error:", e)

try:
    print("Testing gemini-1.5-flash-002 without v1...")
    client3 = genai.Client(api_key=k)
    res = client3.models.generate_content(model="gemini-1.5-flash-002", contents="hi")
    print("default 002 success:", res.text)
except Exception as e:
    print("default 002 error:", e)

