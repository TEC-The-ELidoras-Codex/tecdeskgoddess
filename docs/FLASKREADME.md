# GitHub AI Models Integration for TEC Life & Finance

## Overview
This document provides setup instructions for integrating GitHub's AI model inference endpoint as an alternative or backup to the Gemini API in the TEC Life & Finance project.

## Setup Instructions

### 1. Create a Personal Access Token (PAT)
- Go to GitHub Settings → Developer settings → Personal access tokens
- Create a new token with `models:read` permissions
- Store securely for use in environment variables

### 2. Environment Setup

**PowerShell (Windows):**
```powershell
$Env:GITHUB_TOKEN="<your-github-token-goes-here>"
```

**Command Prompt (Windows):**
```cmd
set GITHUB_TOKEN=<your-github-token-goes-here>
```

**Bash (Linux/Mac):**
```bash
export GITHUB_TOKEN="<your-github-token-goes-here>"
```

### 3. Install Dependencies
```bash
pip install openai
```

### 4. Basic Implementation

```python
import os
from openai import OpenAI

# GitHub AI configuration
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"  # Available models: gpt-4o, gpt-4o-mini, phi-3-mini, etc.

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant for TEC Life & Finance.",
        },
        {
            "role": "user",
            "content": "Help me analyze my journal entry for patterns.",
        }
    ],
    temperature=1.0,
    top_p=1.0,
    model=model
)

print(response.choices[0].message.content)
```

## Integration with TEC Architecture

### Recommended Integration Points
1. **AI Chatbot Module** (`tec_tools/agentic_processor.py`)
   - Use as fallback when Gemini API is unavailable
   - Implement model switching logic

2. **Journaling Analysis** (`tec_tools/lore_extractor.py`)
   - Use for text analysis and insight generation
   - Compare results with Gemini for best output

3. **Finance Analysis**
   - Use for crypto market analysis and portfolio insights
   - Leverage for financial advice generation

### Implementation Strategy
```python
# Example fallback implementation
class AIProcessor:
    def __init__(self):
        self.github_client = self._setup_github_client()
        self.gemini_client = self._setup_gemini_client()
    
    def process_request(self, messages, use_github=False):
        try:
            if use_github or not self.gemini_available():
                return self._github_request(messages)
            else:
                return self._gemini_request(messages)
        except Exception as e:
            # Fallback to alternative provider
            return self._fallback_request(messages)
```

## Benefits for TEC Project
- **Redundancy**: Backup when primary AI services are down
- **Cost Management**: GitHub free tier for development/testing
- **Model Diversity**: Access to different AI models for comparison
- **Integration**: Seamless OpenAI SDK compatibility

## Rate Limits & Scaling
- Free tier has limitations suitable for prototyping
- For production scale, consider Azure AI Foundry integration
- Monitor usage and implement appropriate rate limiting

## Security Considerations
- Store PAT in environment variables, never in code
- Use `.env` files for local development
- Implement proper error handling for authentication failures

## Next Steps
1. Integrate into existing `tec_tools/agentic_processor.py`
2. Add configuration management for multiple AI providers
3. Implement intelligent model selection based on task type
4. Add monitoring and fallback mechanisms
