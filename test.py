from langchain_ollama import OllamaLLM

def test_model(model_name):
    """Test if a model can run on this system"""
    print(f"\nTesting {model_name}...")
    try:
        llm = OllamaLLM(model=model_name, temperature=0.3)
        response = llm.invoke("Say 'Hello'")
        print(f"✓ {model_name} works! Response: {response[:50]}")
        return True
    except Exception as e:
        print(f"✗ {model_name} failed: {str(e)[:100]}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Testing Available Models")
    print("="*60)
    
    # List of models to test (from smallest to largest)
    models = [
        "tinyllama",   # ~637MB
        "phi3",        # ~2.3GB  
        "mistral",     # ~4.1GB
        "qwen3",       # ~5.5GB
    ]
    
    working_models = []
    
    for model in models:
        if test_model(model):
            working_models.append(model)
    
    print("\n" + "="*60)
    if working_models:
        print("✓ Working models on your system:")
        for m in working_models:
            print(f"  - {m}")
        print(f"\nRecommended: Use '{working_models[0]}' for best performance")
        print(f"Update your .env file: OLLAMA_MODEL={working_models[0]}")
    else:
        print("✗ No models working. Please install a model:")
        print("  ollama pull tinyllama")