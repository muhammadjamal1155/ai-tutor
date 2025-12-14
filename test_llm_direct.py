from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import config
import os

print(f"Key loaded: {config.GOOGLE_API_KEY[:5]}...")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3, 
        google_api_key=config.GOOGLE_API_KEY
    )
    print("LLM Initialized. Invoking...")
    response = llm.invoke("Say hello")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"LLM Failed: {e}")

