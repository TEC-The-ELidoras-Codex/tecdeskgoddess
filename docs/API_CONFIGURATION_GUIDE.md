# 🔑 TEC: BITLYFE API Configuration Guide

## ⚠️ SECURITY FIRST!
**NEVER commit API keys to git repositories!** Always use environment variables.

## 📋 Required API Keys for Full TEC Functionality

### 1. 🤖 **Primary AI Providers** (Choose at least 2 for redundancy)

#### **OpenAI API** 
- **Where to get**: https://platform.openai.com/api-keys
- **Environment variable**: `OPENAI_API_KEY=sk-...`
- **Used for**: Advanced reasoning, GPT-4, DALL-E image generation
- **Cost**: Pay-per-use (varies by model)

#### **Anthropic Claude API**
- **Where to get**: https://console.anthropic.com/
- **Environment variable**: `ANTHROPIC_API_KEY=sk-ant-...`
- **Used for**: Safety-focused AI, complex analysis, constitutional AI
- **Cost**: Pay-per-use

#### **XAI (Grok) API**
- **Where to get**: https://console.x.ai/
- **Environment variable**: `XAI_API_KEY=xai-...`
- **Used for**: Uncensored AI responses, real-time data access
- **Cost**: Pay-per-use

#### **Google Gemini API**
- **Where to get**: https://makersuite.google.com/app/apikey
- **Environment variable**: `GEMINI_API_KEY=AIza...`
- **Used for**: Multimodal AI, long context, free tier available
- **Cost**: Free tier + pay-per-use

### 2. 🏢 **GitHub AI Models** (Backup/Enterprise)
- **Where to get**: https://github.com/settings/tokens
- **Environment variable**: `GITHUB_TOKEN=ghp_...`
- **Required permissions**: `models:read`
- **Used for**: Coding assistance, technical tasks, fallback AI
- **Cost**: Included with GitHub Pro/Team

### 3. ☁️ **Azure AI Services** (Your TEC BITLYFE TSC Resource)
- **Where to get**: Azure Portal → Cognitive Services → Keys and Endpoint
- **Environment variables**:
  ```bash
  AZURE_API_KEY_1=your_primary_key
  AZURE_API_KEY_2=your_secondary_key
  AZURE_COGNITIVE_SERVICES_ENDPOINT=https://tec-bitlyfe-tsc-resource.cognitiveservices.azure.com/
  ```
- **Used for**: Speech-to-text, translation, document intelligence, search
- **Cost**: Free tier available + pay-per-use

### 4. 🎵 **Optional Multimedia Services**

#### **ElevenLabs API** (Voice/Audio)
- **Where to get**: https://elevenlabs.io/
- **Environment variable**: `ELEVENLABS_API_KEY=sk_...`
- **Used for**: High-quality text-to-speech, voice cloning
- **Cost**: Free tier + subscription

### 5. 💰 **Financial Data APIs** (Choose one or multiple)

#### **CoinGecko API** (Recommended)
- **Where to get**: https://www.coingecko.com/en/api
- **Environment variable**: `COINGECKO_API_KEY=CG-...`
- **Used for**: Crypto prices, market data, comprehensive coverage
- **Cost**: Free tier (10k calls/month) + paid tiers

#### **CoinMarketCap API**
- **Where to get**: https://coinmarketcap.com/api/
- **Environment variable**: `COINMARKETCAP_API_KEY=...`
- **Used for**: Alternative crypto data source
- **Cost**: Free tier + paid tiers

## 🚀 Quick Setup Instructions

### Step 1: Copy Environment Template
```bash
cp config/.env.template .env
```

### Step 2: Edit .env with Your Keys
```bash
# Open in your preferred editor
code .env
# OR
notepad .env
```

### Step 3: Add to .gitignore (CRITICAL!)
Make sure `.env` is in your `.gitignore` file:
```
.env
*.env
!.env.template
```

### Step 4: Test Configuration
```bash
python scripts/test_api_keys.py
```

## 💡 Pro Tips

### **Cost Optimization**
- Start with **Google Gemini** (has generous free tier)
- Use **GitHub AI Models** for coding tasks (free with GitHub Pro)
- Add **XAI** for uncensored responses when needed
- Use **Azure** for specialized tasks (speech, translation)

### **Censorship Resistance**
- Configure multiple providers for automatic fallback
- Local LLMs (future): Ultimate censorship resistance
- XAI: Known for minimal content restrictions

### **Security Best Practices**
- Rotate API keys regularly
- Use separate keys for development/production
- Monitor usage in provider dashboards
- Set spending limits where available

## 🔧 TEC System Commands

### Start with API Validation
```bash
python main.py --validate-apis
```

### Start in Development Mode
```bash
python main.py --dev
```

### Check System Status
```bash
python scripts/status_check.py
```

---

*"Unfettered Access Shall Be Maintained" - The Creator's Rebellion*
