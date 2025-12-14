print("1. Importing langchain...")
import langchain
print(f"   Success. Version: {langchain.__version__}")

print("2. Importing langchain.chains...")
try:
    import langchain.chains
    print("   Success.")
except ImportError as e:
    print(f"   FAILED: {e}")

print("3. Importing create_stuff_documents_chain...")
try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
    print("   Success.")
except ImportError as e:
    print(f"   FAILED: {e}")

print("4. Importing create_retrieval_chain...")
try:
    from langchain.chains import create_retrieval_chain
    print("   Success (Main path).")
except ImportError as e:
    print(f"   Main path FAILED: {e}")
    try:
        from langchain.chains.retrieval import create_retrieval_chain
        print("   Success (Fallback path).")
    except ImportError as e2:
        print(f"   Fallback path FAILED: {e2}")
