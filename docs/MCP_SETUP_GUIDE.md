# 🎯 TEC: BITLYFE MCP Setup Guide

## 🔥 GitHub Copilot + Multi-Provider AI Integration

This guide shows how to set up the complete TEC: BITLYFE system with GitHub Copilot MCP integration and multi-provider AI support.

## 🏗️ Architecture Overview

```
TEC: BITLYFE System
├── GitHub Copilot (MCP Client)
├── TEC Agentic Processor (MCP Server)
├── Multi-Provider AI Backend
│   ├── Google Gemini
│   ├── XAI Grok
│   ├── Anthropic Claude
│   ├── OpenAI
│   ├── GitHub AI
│   └── Azure AI Services
├── Memory & Analytics System
├── Crypto Integration
└── Enhanced Chat Interface
```

## 🛠️ Prerequisites

1. **GitHub Copilot Subscription** - Active subscription required
2. **VS Code** - Latest version with GitHub Copilot extension
3. **Python 3.8+** - For the MCP server and backend
4. **API Keys** - For AI providers (see configuration section)
5. **Git** - For version control and MCP setup

## 📦 Installation Steps

### 1. Clone and Setup Repository

```bash
git clone https://github.com/TEC-The-ELidoras-Codex/tecdeskgoddess.git
cd tecdeskgoddess
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the template
cp .env.template .env

# Edit .env file with your API keys
GOOGLE_API_KEY=your_gemini_key_here
XAI_API_KEY=your_xai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token_here
AZURE_OPENAI_KEY=your_azure_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
```

### 3. Configure MCP Integration

Create `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "tec-agentic-processor": {
      "command": "python",
      "args": ["src/tec_tools/agentic_processor.py"],
      "env": {
        "PYTHONPATH": "."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

## API Provider Status

### ✅ Working Providers

- **Gemini**: `GOOGLE_API_KEY` (configured via environment)
- **XAI**: `XAI_API_KEY` (configured via environment)
- **Anthropic**: Configured and ready
- **OpenAI**: Configured and ready
- **GitHub AI**: Ready with your token

### 🔧 Azure Configuration

- **Primary**: TEC-BITLYFE-TSC endpoint
- **Fallback**: Secondary Azure endpoint
- **Models**: GPT-4, GPT-3.5-turbo support

## 🧪 Testing Setup

### Test XAI API

```bash
curl "https://api.x.ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "messages": [{"role": "user", "content": "Hello from TEC: BITLYFE!"}],
    "model": "grok-2-1212",
    "stream": false,
    "temperature": 0.7
  }'
```

### Test Local API

```bash
# Start the Flask server
python main.py

# Test the chat endpoint
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello TEC!", "provider": "gemini"}'
```

## 🚀 Using the System

### 1. Start the Backend

```bash
python main.py
```

### 2. Open Chat Interface

```bash
# Open in browser
tec_chat.html
```

### 3. Use GitHub Copilot

- Open VS Code in the project directory
- GitHub Copilot will automatically use the MCP configuration
- Ask Copilot about TEC features, AI integration, or development tasks

## 🎯 Key Features

### Multi-Provider AI

- Intelligent fallback between providers
- Provider-specific optimizations
- Rate limiting and error handling

### Memory System

- Conversation history persistence
- Context-aware responses
- User preference learning

### Analytics

- API usage tracking
- Response time monitoring
- Provider performance metrics

### Security

- API key protection
- Request validation
- Rate limiting

## 🔧 Troubleshooting

### Common Issues

1. **MCP Not Working**
   - Check `.vscode/mcp.json` exists
   - Restart VS Code
   - Verify Python path

2. **API Keys Not Working**
   - Check `.env` file exists
   - Verify API key format
   - Test individual providers

3. **Flask Server Issues**
   - Check port 5000 availability
   - Verify dependencies installed
   - Check logs for errors

## 📚 Next Steps

1. **Expand AI Capabilities**: Add more providers
2. **Voice Integration**: Speech-to-text features
3. **Crypto Portfolio**: Real-time tracking
4. **Gamification**: Achievement system

---

**TEC: BITLYFE** - *The Creator's Rebellion for Digital Sovereignty* 🏴‍☠️
