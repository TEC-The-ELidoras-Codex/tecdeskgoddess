# TEC: BITLYFE Command Reference

This guide provides the exact commands needed to configure, start, manage, and stop the TEC system.

## 🔑 API Configuration (FIRST TIME SETUP)

### 1. Configure Your API Keys (Required)
```powershell
python scripts/configure_apis.py
```
**What it does:** Interactive wizard to set up your API keys securely.

### 2. Test API Configuration
```powershell
python scripts/test_api_keys.py
```
**What it does:** Validates all configured API keys are working properly.

### 3. View Configuration Guide
```powershell
# Open the comprehensive API guide
code docs/API_CONFIGURATION_GUIDE.md
```

## 🚀 Quick Start Commands

### 1. System Startup (Recommended)
```powershell
python main.py
```
**What it does:** Complete startup with dependency checking, environment validation, and server launch.

### 2. Alternative Startup Methods

#### Basic Flask Server Only
```powershell
python -m flask --app src.tec_tools.api run --host=0.0.0.0 --port=8000
```

#### Manual Startup Script
```powershell
python scripts/tec_startup.py
```

#### Simple Startup
```powershell
python tec_simple_startup.py
```

---

## 🔧 System Management Commands

### Check System Health
```powershell
curl http://localhost:8000/health
```
**Expected Response:** `{"service":"TEC API","status":"ok"}`

### Test AI Chat Endpoint
```powershell
curl -X POST http://localhost:8000/ai_chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```

### Check Running Processes
```powershell
Get-Process python
```

### View System Logs
```powershell
Get-Content tec_startup.log -Tail 20
```

---

## 🛑 Shutdown Commands

### Safe Shutdown (Recommended)
```powershell
python tec_safe_shutdown.py
```
**What it does:** Gracefully terminates all TEC processes and cleans up resources.

### Simple Shutdown
```powershell
python tec_simple_shutdown.py
```

### Manual Process Termination
```powershell
# Find Python processes
Get-Process python | Where-Object {$_.ProcessName -eq "python"}

# Kill specific process by ID (replace XXXX with actual PID)
Stop-Process -Id XXXX -Force
```

---

## 📁 File Management Commands

### Clean Logs
```powershell
Remove-Item *.log -Force
```

### Reset Environment
```powershell
python scripts/reset_and_test.py
```

### Git Status Check
```powershell
git status
```

---

## 🌐 Access Points

### Web Interface
- **Main Interface:** http://localhost:8000/
- **Complete Interface:** http://localhost:8000/tec_complete_interface.html
- **Simple Chat:** http://localhost:8000/tec_chat.html

### API Endpoints
- **Health Check:** http://localhost:8000/health
- **AI Chat:** http://localhost:8000/ai_chat (POST)
- **Status:** http://localhost:8000/status

---

## 🔍 Troubleshooting Commands

### Check Port Usage
```powershell
netstat -ano | findstr :8000
```

### Install Dependencies
```powershell
pip install -r requirements.txt
pip install openai
```

### Environment Setup
```powershell
# Copy template (first time only)
Copy-Item config/.env.template .env

# Edit environment file
notepad .env
```

### Python Environment Check
```powershell
python --version
pip list | findstr flask
```

---

## 📋 Daily Workflow

### Morning Startup
1. Open PowerShell in project directory
2. Run: `python main.py`
3. Wait for "Server running on http://0.0.0.0:8000"
4. Open browser to http://localhost:8000/

### Evening Shutdown
1. Close browser tabs
2. Run: `python tec_safe_shutdown.py`
3. Confirm all processes terminated

---

## 🆘 Emergency Commands

### Force Kill All Python
```powershell
Get-Process python | Stop-Process -Force
```

### Clear All Logs
```powershell
Remove-Item *.log, logs/*.log -Force -ErrorAction SilentlyContinue
```

### Reset Git (if needed)
```powershell
git reset --hard HEAD
git clean -fd
```

---

## 🔐 Security Notes

- Never commit `.env` files to git
- Azure credentials should only be in `.env` file
- Use `.env.template` as reference for required variables
- Regularly rotate API keys

---

## 📞 Need Help?

If commands fail:
1. Check Python is installed: `python --version`
2. Verify in correct directory: `ls main.py` should exist
3. Check `.env` file exists and has Azure credentials
4. Review logs: `Get-Content tec_startup.log`

---

*Last Updated: January 2025*
