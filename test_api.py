import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Manually set key for test
os.environ["GOOGLE_API_KEY"] = "AIzaSyBSec5hVM28bwUCxGDXkOgrKXSjJntw5mQ"

def test_embedding():
    print("Testing Embedding with text-embedding-004...")
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vec = embeddings.embed_query("Hello world")
        print(f"Success! Vector length: {len(vec)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_embedding()
