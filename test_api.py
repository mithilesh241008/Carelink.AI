from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API Loaded:", bool(api_key))

if api_key:
    print("First 10 chars:", api_key[:10])