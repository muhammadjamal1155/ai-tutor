import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import config
from src.agent.tutor import TutorAgent
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

def test_setup():
    print("Testing OpenAI Setup...")
    
    # 1. Check Key
    if not config.OPENAI_API_KEY:
        print("FAIL: OPENAI_API_KEY not found in config.")
        return
    print(f"PASS: API Key found: {config.OPENAI_API_KEY[:5]}...")

    # 2. Check Embeddings Init
    try:
        embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        print(f"PASS: OpenAIEmbeddings initialized with model {config.EMBEDDING_MODEL}")
    except Exception as e:
        print(f"FAIL: Embeddings Init Error: {e}")

    # 3. Check LLM Init
    try:
        llm = ChatOpenAI(
            model=config.MODEL_NAME, 
            temperature=0.3, 
            openai_api_key=config.OPENAI_API_KEY
        )
        print(f"PASS: ChatOpenAI initialized with model {config.MODEL_NAME}")
    except Exception as e:
        print(f"FAIL: LLM Init Error: {e}")

    # 4. Check Agent Init
    try:
        agent = TutorAgent()
        print("PASS: TutorAgent initialized successfully.")
    except Exception as e:
        print(f"FAIL: TutorAgent Init Error: {e}")

    print("Verification Complete.")

if __name__ == "__main__":
    test_setup()
