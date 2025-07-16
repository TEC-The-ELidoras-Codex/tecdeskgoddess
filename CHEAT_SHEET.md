# 🎯 TEC: BITLYFE Command Cheat Sheet
*The Creator's Rebellion - Complete Command Reference*

## 🚀 STARTUP COMMANDS

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
