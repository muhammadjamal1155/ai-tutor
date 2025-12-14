import langchain
import inspect
import pkgutil

print(f"LangChain Version: {langchain.__version__}")

def list_submodules(package_name):
    try:
        package = __import__(package_name, fromlist=[''])
        print(f"\nSubmodules of {package_name}:")
        if hasattr(package, '__path__'):
            for _, name, _ in pkgutil.iter_modules(package.__path__):
                print(f" - {name}")
        else:
            print(" (Not a package or no __path__)")
    except ImportError as e:
        print(f"Error importing {package_name}: {e}")

list_submodules("langchain")
list_submodules("langchain.chains")
