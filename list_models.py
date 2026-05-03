import os
from google import genai

k = "AIzaSyDUuW6OHz71H64ndmTAY4K-OVqg00-HMsQ"
client = genai.Client(api_key=k)

try:
    print("Available models:")
    for m in client.models.list():
        print(m.name)
except Exception as e:
    print("Error listing models:", e)
