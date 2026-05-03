import os
from google import genai

keys = [
    "AIzaSyDVcFTC_tCPMKKsufazC6yG7MMISkktU4o",
    "AIzaSyDVcFTC_tCPMKKsufazC6yG7MMlSkktU4o",
    "AIzaSyDVcFTC_tCPMKKSufazC6yG7MMISkktU4o",
    "AIzaSyDVcFTC_tCPMKKSufazC6yG7MMlSkktU4o",
    "AIzaSyDVcFTC_tCPMKKsufazC6yG7MM1SkktU4o",
    "AIzaSyDVcFTC_tCPMKKsufazC6yG7MMISkktU40",
]

for k in keys:
    try:
        client = genai.Client(api_key=k)
        client.models.generate_content(model="gemini-1.5-flash", contents="hi")
        print(f"SUCCESS: {k}")
        break
    except Exception as e:
        if "API key not valid" in str(e):
            print(f"FAILED: {k}")
        else:
            print(f"OTHER ERROR FOR {k}: {e}")
