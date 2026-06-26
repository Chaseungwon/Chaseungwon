import os
from dotenv import load_dotenv

load_dotenv()

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
if not HEYGEN_API_KEY:
    raise ValueError("Please set HEYGEN_API_KEY in .env or as environment variable")

print(f"HeyGen API key loaded: {HEYGEN_API_KEY[:10]}...")
