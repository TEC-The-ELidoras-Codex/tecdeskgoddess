# TEC PROJECT: STARTUP & SHUTDOWN CHEAT SHEET

## 🔄 STARTUP PROCESS

### Method 1: Simple Startup (Recommended)
```powershell
# Navigate to project
cd "C:\Users\Ghedd\TEC_CODE\tecdeskgoddess"

# Start TEC system
python tec_simple_startup.py

# Wait for "SUCCESS: TEC Web Interface is running!" message
# Then open browser to: http://localhost:8000
```

### Method 2: Full MCP System (Advanced)
```powershell
# Start full MCP ecosystem (requires all API keys)
python tec_startup.py
```

### Method 3: Quick Test
```powershell
# Just run the API server directly
python simple_api.py
```

---

## 🛑 SHUTDOWN PROCESS

### Safe Shutdown (Always do this!)
```powershell
# In the terminal running TEC:
Ctrl + C

# Wait for "All services stopped" message
# Then close terminal
```

### Emergency Shutdown
```powershell
# If system is stuck, kill Python processes:
taskkill /F /IM python.exe

# Check if ports are free:
netstat -ano | findstr :8000
```

---

## 🔍 STATUS CHECKS

### Quick Health Check
```powershell
# Test API endpoint
curl http://localhost:8000/health

# Or open in browser:
# http://localhost:8000/health
```

### Process Check
```powershell
# See running Python processes
tasklist | findstr python

# Check specific ports
netstat -ano | findstr :8000
netstat -ano | findstr :5000
```

---

## 📂 PROJECT STRUCTURE

### Workspace Method (Recommended)
✅ **Open VS Code Workspace**: Use the `.code-workspace` file
- Keeps all settings intact
- Preserves terminal configurations  
- Maintains project context

### Folder Method (Alternative)
⚠️ **Open Folder**: Open `tecdeskgoddess` folder directly
- May lose some settings
- Need to reconfigure terminals
- Less reliable for complex projects

---

## 💾 COMMIT & SAVE PROCESS

### Before Shutdown (Always do this!)
```powershell
# 1. Stop TEC system first
Ctrl + C

# 2. Save all files in VS Code
Ctrl + S (or Ctrl + K, S for all)

# 3. Commit changes
git add .
git commit -m "TEC system updates - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main
```

### Emergency Save (If system is stuck)
```powershell
# Force stop everything
taskkill /F /IM python.exe

# Quick commit
git add -A
git commit -m "Emergency save before shutdown"
git push
```

---

## 🔧 TROUBLESHOOTING

### Common Issues

1. **Port 8000 in use**
   ```powershell
   netstat -ano | findstr :8000
   taskkill /PID <PID_NUMBER> /F
   ```

2. **Can't connect to API**
   - Check if `tec_simple_startup.py` is running
   - Verify health endpoint: http://localhost:8000/health
   - Check firewall settings

3. **Multiple Python processes**
   ```powershell
   tasklist | findstr python
   taskkill /F /IM python.exe
   ```

4. **VS Code webview errors**
   - Close Simple Browser tabs
   - Restart VS Code
   - Use external browser instead

---

## 📱 ACCESS METHODS

### Web Interfaces
- **Main Interface**: http://localhost:8000
- **Enhanced UI**: http://localhost:8000/tec_complete_interface.html
- **Simple Chat**: http://localhost:8000/tec_chat.html
- **Health Check**: http://localhost:8000/health

### VS Code Integration
- Simple Browser (built-in)
- External browser (more reliable)
- Terminal commands

---

## 🎯 BEST PRACTICES

### Always Do:
1. ✅ Use `Ctrl+C` to stop servers gracefully
2. ✅ Save files before shutdown (`Ctrl+S`)
3. ✅ Commit changes before closing (`git add . && git commit`)
4. ✅ Check process status before starting new instances
5. ✅ Use workspace file for VS Code

### Never Do:
1. ❌ Force close terminal without stopping servers
2. ❌ Run multiple instances on same port
3. ❌ Forget to commit before shutdown
4. ❌ Leave Python processes running overnight
5. ❌ Modify files without saving first

---

## 🚨 EMERGENCY PROCEDURES

### System Frozen
```powershell
# Force kill all Python
taskkill /F /IM python.exe

# Emergency commit
git add -A && git commit -m "Emergency save" && git push
```

### Can't Access Git
```powershell
# Check git status
git status

# Force add everything
git add -A --force

# Commit with timestamp
git commit -m "Forced save $(Get-Date)"
```

### VS Code Issues
1. Close all terminals
2. Close VS Code
3. Kill Python processes
4. Restart VS Code
5. Open workspace file

---

## 📋 QUICK REFERENCE

| Action | Command |
|--------|---------|
| Start TEC | `python tec_simple_startup.py` |
| Stop TEC | `Ctrl + C` |
| Health Check | `curl http://localhost:8000/health` |
| Kill Python | `taskkill /F /IM python.exe` |
| Check Ports | `netstat -ano \| findstr :8000` |
| Quick Commit | `git add . && git commit -m "Update"` |
| Force Save | `git add -A && git commit -m "Save"` |

---

**Remember: Always shutdown gracefully and commit your work!**

*The Creator's Rebellion - TEC: BITLYFE*
