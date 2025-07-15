# 🔒 TEC Security Guide - Protecting Your API Keys

## 🚨 CRITICAL SECURITY RULES

### ❌ NEVER DO THESE:
1. **Never commit .env files** with real API keys
2. **Never put API keys in code files** (Python, JavaScript, etc.)
3. **Never put API keys in documentation** (README, markdown files)
4. **Never share screenshots** showing API keys
5. **Never put API keys in issue descriptions** or comments

### ✅ ALWAYS DO THESE:
1. **Use .env file** for all secrets (already in .gitignore)
2. **Use .env.template** for sharing configuration structure
3. **Run security checks** before committing: `python scripts/security_check.py`
4. **Regenerate exposed keys** immediately if accidentally committed
5. **Use environment variables** in production

## 🛡️ Security Features Implemented

### 1. Automatic Protection
- **Pre-commit hook**: Blocks commits with API keys
- **Security scanner**: Detects exposed keys in all files
- **.gitignore**: Prevents .env from being tracked

### 2. Safe Configuration
- **.env.template**: Safe template for sharing
- **Environment loading**: Code reads from .env safely
- **Key rotation support**: Easy to update keys

### 3. Detection Patterns
Our security scanner detects:
- OpenAI keys (`sk-...`)
- Anthropic keys (`sk-ant-api...`)
- XAI keys (`xai-...`)
- Google API keys (`AIza...`)
- GitHub tokens (`github_pat_...`)
- Azure keys (64-char + AAAA pattern)
- ElevenLabs keys (`sk_...`)
- UUIDs (subscription IDs)

## 🔧 Commands

### Security Check (Run Before Committing)
```bash
python scripts/security_check.py
```

### Setup New Environment
```bash
# Copy template
cp .env.template .env

# Edit with your real keys
notepad .env  # or your preferred editor

# Verify security
python scripts/security_check.py
```

### If Keys Are Exposed
```bash
# 1. Remove from files immediately
# 2. Regenerate all exposed keys
# 3. Update .env with new keys
# 4. Run security check
python scripts/security_check.py

# 5. Commit the fix
git add -A
git commit -m "Security: Remove exposed API keys"
```

## 🎯 Best Practices

### For Development
- Use .env for all secrets
- Never hardcode API keys
- Test with security_check.py
- Use meaningful variable names

### For Production  
- Use Azure Key Vault or similar
- Set environment variables securely
- Monitor for exposed keys
- Rotate keys regularly

### For Collaboration
- Share .env.template only
- Document required keys
- Never share actual keys in chat/email
- Use secure key sharing tools if needed

## 🚨 Emergency Response

### If API Keys Are Compromised:
1. **Immediately revoke/regenerate** all exposed keys
2. **Check all affected services** for unauthorized usage
3. **Update .env** with new keys
4. **Review access logs** for suspicious activity
5. **Update any hardcoded references**

## 📋 Security Checklist

Before every commit:
- [ ] Run `python scripts/security_check.py`
- [ ] Verify no API keys in new files
- [ ] Check that .env is not staged for commit
- [ ] Ensure sensitive data uses environment variables

Remember: **"Better safe than sorry"** - Your API keys are the keys to your digital kingdom!

---
*TEC: BITLYFE IS THE NEW SHIT - The Creator's Rebellion Security Protocol*
