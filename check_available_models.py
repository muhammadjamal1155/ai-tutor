#!/usr/bin/env python3
"""
Quick script to check available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment")
    exit(1)

print(f"Using API Key: {api_key[:10]}...")

# Configure Gemini
genai.configure(api_key=api_key)

print("\nAvailable Gemini Models:")
print("=" * 50)

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print("-" * 30)
except Exception as e:
    print(f"Error listing models: {e}")