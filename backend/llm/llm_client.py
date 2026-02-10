import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)


class LLMClient:
    def __init__(self):
        self.model = "gemini-2.5-flash"
        # INCREASED OUTPUT LIMIT TO ALLOW FULL REPORTS
        self.config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=2048, 
        )

    def generate(self, prompt: str) -> str:
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.config,
            )

            if not response or not response.text:
                return "The requested information is not available in the provided documents."

            return response.text.strip()
            
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return "An error occurred while generating the response."