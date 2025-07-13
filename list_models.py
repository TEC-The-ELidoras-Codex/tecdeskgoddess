import os
from openai import OpenAI

def list_available_models():
    """List available models from GitHub AI"""
    try:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("❌ GITHUB_TOKEN environment variable not set!")
            return
            
        endpoint = "https://models.github.ai/inference"

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        print("🔍 Fetching available models...")
        models = client.models.list()
        
        print("✅ Available models:")
        for model in models.data:
            print(f"  - {model.id}")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()
