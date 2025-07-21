# 🎯 TEC Enhanced Persona System - Complete Cheatsheet
*The Creator's Rebellion - Enhanced with Persona System*

## 📋 **Current System Status**
✅ **TEC Clean Architecture Protocol TEC_ARCH_071925_V1** - 100% Complete  
✅ **Mobile Optimization** - Responsive design, touch controls  
✅ **Audio Integration** - TTS, voice input, character voices  
✅ **Visual Enhancements** - Themes, animations, particles  
✅ **Web3 Authentication** - MetaMask integration, access tiers  
✅ **Character System** - Polkin, Mynx, Kaelen with full lore  
✅ **AI Personality Control** - Creativity, memory, reasoning modes  
✅ **Gamification** - BITL tokens, quests, XP system  
✅ **Local AI Integration** - Ollama, RAG, Docker, MCP support  
✅ **Image Generation** - Draw Things, Docker Stable Diffusion  

## 🛠️ **Quick Start Commands**
```bash
# TEC Clean Architecture System
python tec_enhanced_api.py           # Start enhanced API with Clean Architecture
python test_ollama_setup.py          # Test local AI (Ollama) setup
python demo_rag_system.py           # Demo RAG knowledge system

# Legacy Persona System  
python tec_persona_api.py           # Start persona API server
python -m http.server 8000          # Start complete interface server

# Testing and Setup
python scripts/test_persona_system.py
python scripts/initialize_character_lore.py

# Local AI Commands (Ollama)
ollama --version                    # Check Ollama installation
ollama pull llama3.2:3b            # Install recommended model
ollama run llama3.2:3b "Hello!"    # Test model

# Docker Stack (Advanced)
docker-compose up -d                # Start full AI stack

# Web Interfaces
start tec_enhanced_interface.html   # Enhanced UI (Persona + Audio + Visual)
start tec_complete_interface.html   # Complete UI (Web3 + Gamification)
```

## 📁 **File Structure**
```
tecdeskgoddess/
├── TEC_COMPLETE_AI_SETUP_GUIDE.md  # Complete AI setup guide
├── tec_enhanced_api.py             # Enhanced API with Clean Architecture
├── test_ollama_setup.py            # Local AI testing script
├── demo_rag_system.py              # RAG knowledge demo
├── core/                           # Clean Architecture - Core Layer
│   ├── player.py                   # Player entity
│   ├── npc.py                      # NPC entity  
│   ├── game_world.py               # Game world entity
│   └── item.py                     # Item entity
├── services/                       # Clean Architecture - Service Layer
│   ├── mcp_service.py              # AI/MCP integration
│   ├── player_service.py           # Player business logic
│   └── npc_service.py              # NPC business logic
├── facade/                         # Clean Architecture - Facade Layer
│   └── tec_facade.py               # Unified game interface
├── tec_enhanced_interface.html     # Enhanced UI (Persona + Audio + Visual)
├── tec_complete_interface.html     # Complete UI (Web3 + Gamification)  
├── tec_persona_api.py             # Legacy persona API server
├── src/tec_tools/
│   ├── persona_manager.py          # Database layer
│   └── agentic_processor.py        # AI processing
├── assets/
│   ├── css/persona_ui.css
│   └── js/persona_manager.js
├── data/
│   ├── tec_database.db            # SQLite database
│   └── tec_knowledge_base.json    # RAG knowledge base
└── docker/                       # Docker deployment files
```

## �️ **TEC Clean Architecture Protocol TEC_ARCH_071925_V1**

### **4-Layer Architecture**
```
┌─────────────────────────────────────────┐
│               UI Layer                  │ ← Flask API (tec_enhanced_api.py)
├─────────────────────────────────────────┤
│             Facade Layer                │ ← GameFacade (unified interface)
├─────────────────────────────────────────┤
│            Service Layer                │ ← Business Logic + AI Integration
├─────────────────────────────────────────┤
│              Core Layer                 │ ← Game Entities (Player, NPC, etc.)
└─────────────────────────────────────────┘
```

### **Clean Architecture Endpoints**
```bash
# System Health
GET  /health                        # Architecture status

# Game Management  
POST /api/game/player/create        # Create player
GET  /api/game/player/{id}          # Get player
POST /api/game/npc/create           # Create NPC
POST /api/game/npc/{id}/dialogue    # Generate NPC dialogue
POST /api/game/world/create         # Create game world
POST /api/game/item/create          # Create item

# AI Integration
POST /api/ai/switch_provider        # Switch AI provider (local/cloud)
POST /api/ai/chat                   # AI chat with context
```

## 🤖 **Local AI Integration (Ollama + RAG)**

### **Ollama Models (Choose based on 12GB RAM)**
```bash
llama3.2:3b    # 2GB - Recommended balance
llama3.2:1b    # 1.3GB - Fastest option  
gemma2:2b      # 1.6GB - Alternative choice
qwen2:1.5b     # 1GB - Compact option
```

### **RAG (Retrieval Augmented Generation)**
- 🧠 AI knows YOUR specific game world
- 📚 Consistent character backgrounds  
- 🎯 Up-to-date game rules and lore
- 🔍 Contextual NPC responses

### **Docker AI Stack**
```bash
docker-compose up -d               # Full AI stack
# Includes: TEC API, Ollama, ChromaDB
```

## 🖼️ **Image Generation Options**
```bash
# Local (Draw Things - you have this)
Draw Things app                    # Direct from Hugging Face

# Docker Stable Diffusion
docker pull stabilityai/stable-diffusion:latest
docker run -p 7860:7860 stabilityai/stable-diffusion:latest

# Ollama (if supported)
ollama pull stable-diffusion
```

## 🔗 **MCP + Hugging Face Integration**
- 🎯 25 minutes daily ZeroGPU compute (H200 hardware)
- 🚀 Access to 500k+ models  
- 🔧 VS Code MCP integration
- 📡 Spaces semantic search

## �🎮 **Interface Comparison**

### **tec_enhanced_interface.html** (Primary)
- ✅ Persona System with Character Lore
- ✅ Mobile Optimization
- ✅ Audio Integration (TTS + Voice Input)
- ✅ Visual Enhancements (Themes + Animations)
- ✅ AI Settings Control
- ✅ Character Selection (Polkin, Mynx, Kaelen)

### **tec_complete_interface.html** (Web3 + Gaming)
- ✅ Web3 Authentication (MetaMask)
- ✅ BITL Token System
- ✅ Quest System with XP
- ✅ Multi-Persona Chat
- ✅ Portfolio Tracking
- ✅ Calendar Integration

## 🚀 **Deployment Options**

### **Option 1: Local Development**
```bash
# Clone and setup
git clone [repository]
cd tecdeskgoddess
pip install -r requirements.txt

# Start API
python tec_persona_api.py

# Open interface
start tec_enhanced_interface.html
```

### **Option 2: Docker (Cross-Platform)**
```bash
# Build container
docker build -t tec-persona .

# Run with data persistence
docker run -p 8000:8000 -v ./data:/app/data tec-persona
```

### **Option 3: Hugging Face Spaces**
```bash
# Deploy to HF Spaces
git push hf main
```

## 🔧 **System Requirements**

### **Backend Dependencies**
```bash
pip install flask flask-cors sqlite3 requests python-dotenv
pip install SpeechRecognition pyttsx3  # For audio features
```

### **Environment Variables**
```bash
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_gemini_key
DATABASE_PATH=./data/tec_database.db
BACKUP_ENABLED=true
```

## 🧪 **Testing Checklist**

### **Core Features**
- [ ] Character selection (Polkin, Mynx, Kaelen)
- [ ] Theme switching with character selection
- [ ] Audio controls (TTS toggle, voice input)
- [ ] AI settings (creativity, memory, reasoning)
- [ ] Mobile responsiveness
- [ ] Persona creation modal

### **Advanced Features**
- [ ] Web3 wallet connection
- [ ] BITL token balance
- [ ] Quest system
- [ ] Chat with authentication
- [ ] Profile persistence

## 📊 **Database Tables**
- `personas` - User persona data
- `characters` - TEC character lore
- `universe_lore` - TEC mythology
- `conversations` - Chat history
- `character_memories` - Context preservation

## 🎯 **Troubleshooting**

### **API Won't Start**
```bash
# Check port availability
netstat -ano | findstr :8000
# Kill conflicting processes
taskkill /PID [PID_NUMBER] /F
```

### **Database Issues**
```bash
# Check database file
dir tec_database.db
# Reinitialize if needed
python scripts/initialize_character_lore.py
```

### **Frontend Not Loading**
```bash
# Verify files exist
dir tec_enhanced_interface.html
dir assets\css\persona_ui.css
```

## 🏆 **Current Status: Production Ready** ✨

---

## 🚀 LEGACY STARTUP COMMANDS

### Quick Start (Recommended)
```bash
py main.py
```

### Manual Start (Alternative)
```bash
py main.py --simple
```

### Start with Debug Mode
```bash
py main.py --debug
```

### Start Simple Mode (No Features)
```bash
py scripts/tec_simple_startup.py
```

## 🔧 DEVELOPMENT COMMANDS

### Security & Safety
```bash
# Check for exposed API keys
py scripts/security_check.py

# Safe shutdown
py tec_safe_shutdown.py

# Terminal cleanup
py scripts/terminal_manager.py
```

### Environment Setup
```bash
# Copy template and setup environment
cp .env.template .env
notepad .env  # Add your API keys

# Test API connections
python scripts/test_apis.py
```

### Database & Data
```bash
# Reset database
python scripts/reset_database.py

# Backup data
python scripts/backup_data.py

# Import data
python scripts/import_data.py
```

## 🌐 WEB ACCESS

### Local Interfaces
- **Simple Chat**: http://localhost:8000
- **Complete Interface**: http://localhost:8000/tec_complete_interface.html ⭐
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/docs

**Note**: Use the Complete Interface for full features including bottom navigation, calendar, finance, and quests!

### API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Chat with Daisy
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Daisy", "user_id": "user123"}'

# BITL Token System
curl http://localhost:8000/api/bitl/balance
curl -X POST http://localhost:8000/api/bitl/earn \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "reason": "test"}'
curl -X POST http://localhost:8000/api/bitl/spend \
  -H "Content-Type: application/json" \
  -d '{"amount": 50, "item": "test_purchase"}'

# Quest System
curl http://localhost:8000/api/quests/list
curl -X POST http://localhost:8000/api/quests/start \
  -H "Content-Type: application/json" \
  -d '{"type": "daily"}'
curl -X POST http://localhost:8000/api/quests/complete \
  -H "Content-Type: application/json" \
  -d '{"questId": "daily_chat"}'

# Upload file
curl -X POST http://localhost:8000/upload \
  -F "file=@yourfile.txt"

# Get user profile
curl http://localhost:8000/user/profile/user123
```

## 📝 GIT COMMANDS

### Basic Git Workflow
```bash
# Check status
git status

# Add files (security check runs automatically)
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### Branch Management
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature
```

### Emergency Git Commands
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Remove file from staging
git reset HEAD filename

# Check commit history
git log --oneline
```

## 🤖 AI COMMANDS

### Chat Commands (In Web Interface)
```
/help              - Show available commands
/status            - System status
/memory            - Show conversation memory
/personality       - Change AI personality
/reset             - Clear conversation
/analyze [url]     - Analyze webpage
/share [content]   - Create shareable link
/quest             - Start new quest
/journal           - Open journal mode
/finance           - Open finance tracker
```

### API Testing Commands
```bash
# Test Gemini
curl -X POST http://localhost:8000/test/gemini

# Test OpenAI
curl -X POST http://localhost:8000/test/openai

# Test XAI
curl -X POST http://localhost:8000/test/xai

# Test Anthropic
curl -X POST http://localhost:8000/test/anthropic
```

## 🛠️ TROUBLESHOOTING

### Common Issues
```bash
# Port already in use
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# Dependencies missing
pip install -r requirements.txt

# Environment issues
python scripts/check_environment.py

# Reset everything
python scripts/full_reset.py
```

### Log Files
```bash
# View logs
Get-Content logs/tec.log -Wait  # PowerShell
tail -f logs/tec.log            # Git Bash

# Clear logs
Remove-Item logs/*.log          # PowerShell
rm logs/*.log                   # Git Bash
```

## 🔧 CUSTOMIZATION

### Change AI Personality
```bash
# Edit personality file
notepad src/personalities/daisy.json

# Or use web interface: Settings → Personality
```

### Add Custom Commands
```python
# Edit src/tec_tools/command_processor.py
# Add new commands in handle_command() function
```

### Modify UI
```javascript
// Edit tec_complete_interface.html
// Customize colors, layout, features
```

## 📊 DATA COMMANDS

### Analytics
```bash
# Generate analytics report
python scripts/generate_analytics.py

# Export data
python scripts/export_data.py --format json
python scripts/export_data.py --format csv

# Import from other platforms
python scripts/import_replika.py
python scripts/import_chatgpt.py
```

### Backup & Restore
```bash
# Full backup
python scripts/backup_full.py

# Restore from backup
python scripts/restore_backup.py backup_20250714.zip

# Sync to cloud
python scripts/sync_azure.py
```

## 🎮 GAMING FEATURES

### Quest System
```
/quest list        - Show active quests
/quest start       - Start new quest
/quest complete    - Complete current quest
/quest abandon     - Abandon quest
```

### RPG Elements
```
/stats             - Show character stats
/level             - Show current level/XP
/inventory         - Show items
/shop              - Open item shop
```

## 🌍 SHARING & SOCIAL

### Share Content
```
/share text "Your message"
/share image path/to/image.jpg
/share url https://example.com
/share post "Social media post"
```

### Memory Management
```
/memory save "Important note"
/memory search "keyword"
/memory delete [id]
/memory export
```

## 🔐 SECURITY COMMANDS

### Immediate Actions
```bash
# Emergency shutdown
Ctrl+C  # In terminal
python scripts/emergency_stop.py

# Security scan
python scripts/security_check.py

# Rotate API keys
python scripts/rotate_keys.py
```

### Permissions
```bash
# Check file permissions
icacls .env

# Set secure permissions
icacls .env /inheritance:r /grant:r "%USERNAME%":F
```

---

## 🎯 QUICK REFERENCE

| Action | Command |
|--------|---------|
| **Start TEC** | `py main.py` |
| **Stop TEC** | `Ctrl+C` or `py tec_safe_shutdown.py` |
| **Check Security** | `py scripts/security_check.py` |
| **Commit Changes** | `git add . && git commit -m "message"` |
| **Test APIs** | `py scripts/test_api_keys.py` |
| **View Logs** | `Get-Content logs/tec.log -Wait` |
| **Reset System** | `py scripts/full_reset.py` |
| **Complete Interface** | `http://localhost:8000/tec_complete_interface.html` |

**Remember**: Always run security checks before committing! 🔒

---
*TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion Command Arsenal*
