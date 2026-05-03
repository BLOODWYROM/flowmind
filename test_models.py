from dotenv import load_dotenv
load_dotenv('backend/.env')

from google import genai
import os

try:
    # Use api_key from environment if not provided automatically
    client = genai.Client()
    print("Models containing 'flash':")
    for m in client.models.list():
        if "flash" in m.name:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
