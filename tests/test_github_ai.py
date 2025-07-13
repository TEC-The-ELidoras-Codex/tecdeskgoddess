import os
from openai import OpenAI

def test_github_ai():
    """Test GitHub AI integration"""
    try:
        # GitHub AI configuration
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("❌ GITHUB_TOKEN environment variable not set!")
            return False
            
        endpoint = "https://models.github.ai/inference"
        model = "gpt-4o-mini"  # Try standard model naming

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        print("🚀 Testing GitHub AI connection...")
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for TEC Life & Finance project.",
                },
                {
                    "role": "user",
                    "content": "Say hello and confirm you're working with the TEC Life & Finance project!",
                }
            ],
            temperature=0.7,
            model=model
        )

        print("✅ GitHub AI Response:")
        print(response.choices[0].message.content)
        return True
        
    except Exception as e:
        print(f"❌ Error testing GitHub AI: {e}")
        return False

if __name__ == "__main__":
    test_github_ai()
