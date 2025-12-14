from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.settings import config

print(f"Key loaded: {config.GOOGLE_API_KEY[:5]}...")

try:
    print("Initializing Embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=config.GOOGLE_API_KEY
    )
    print("Embedding query...")
    vec = embeddings.embed_query("Hello world")
    print(f"Success! Vector length: {len(vec)}")
except Exception as e:
    print(f"Embeddings Failed: {e}")
