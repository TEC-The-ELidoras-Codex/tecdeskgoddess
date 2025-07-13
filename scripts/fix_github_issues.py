#!/usr/bin/env python3
"""
GitHub Issue Resolution Script
Helps resolve persistent GitHub integration issues with TEC project
"""
import os
import json
import subprocess
import sys
from pathlib import Path

def check_github_setup():
    """Check GitHub configuration and suggest fixes"""
    print("=" * 60)
    print("🔍 GitHub Integration Diagnostic")
    print("=" * 60)
    
    issues = []
    fixes = []
    
    # Check Git configuration
    try:
        user_name = subprocess.check_output(['git', 'config', 'user.name'], text=True).strip()
        user_email = subprocess.check_output(['git', 'config', 'user.email'], text=True).strip()
        print(f"✅ Git User: {user_name} <{user_email}>")
    except subprocess.CalledProcessError:
        issues.append("Git user configuration missing")
        fixes.append("Run: git config --global user.name 'Your Name'")
        fixes.append("Run: git config --global user.email 'your.email@example.com'")
    
    # Check GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token and github_token != 'your_github_token_here':
        print("✅ GitHub Token: Set")
        
        # Test token permissions
        try:
            result = subprocess.run([
                'curl', '-H', f'Authorization: token {github_token}',
                'https://api.github.com/user'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                print(f"✅ GitHub API Access: {data.get('login', 'Unknown')}")
            else:
                issues.append("GitHub token authentication failed")
                fixes.append("Verify your GitHub token has correct permissions")
        
        except Exception as e:
            issues.append(f"GitHub API test failed: {e}")
            fixes.append("Check your internet connection and token validity")
    
    else:
        issues.append("GitHub token not set or invalid")
        fixes.append("Set GITHUB_TOKEN environment variable")
        fixes.append("Get token from: https://github.com/settings/tokens")
        fixes.append("Required permissions: repo, workflow, read:org")
    
    # Check repository status
    try:
        remote_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
        print(f"✅ Repository: {remote_url}")
        
        # Check for uncommitted changes
        status = subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
        if status:
            print("⚠️  Uncommitted changes detected:")
            print(status)
            fixes.append("Commit or stash your changes: git add . && git commit -m 'Update'")
        else:
            print("✅ Working directory clean")
            
    except subprocess.CalledProcessError:
        issues.append("Not in a Git repository or no remote origin")
        fixes.append("Initialize Git: git init")
        fixes.append("Add remote: git remote add origin <your-repo-url>")
    
    # Check Copilot configuration
    copilot_config = Path('.github/copilot/mcp.json')
    if copilot_config.exists():
        print("✅ Copilot MCP configuration exists")
        try:
            with open(copilot_config) as f:
                config = json.load(f)
                print(f"✅ MCP Servers configured: {len(config.get('servers', {}))}")
        except Exception as e:
            issues.append(f"Copilot configuration invalid: {e}")
            fixes.append("Fix .github/copilot/mcp.json syntax")
    else:
        issues.append("Copilot MCP configuration missing")
        fixes.append("Create .github/copilot/mcp.json with MCP server definitions")
    
    # Print summary
    print("\n" + "=" * 60)
    if issues:
        print("❌ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n🔧 SUGGESTED FIXES:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
    else:
        print("✅ ALL CHECKS PASSED!")
        print("Your GitHub integration should be working correctly.")
    
    print("=" * 60)
    return len(issues) == 0

def create_github_issue():
    """Create a test GitHub issue to verify integration"""
    print("\n🚀 Creating Test GitHub Issue...")
    
    issue_data = {
        "title": "Test TEC Copilot Integration - Automated",
        "body": '''# TEC Copilot Integration Test

This is an automated test issue to verify GitHub Copilot integration with the TEC MCP ecosystem.

## Test Requirements
- [ ] Test MCP server connectivity
- [ ] Verify context gathering from all TEC modules
- [ ] Generate a simple feature implementation
- [ ] Validate AI code generation capabilities

## Context
- **Project**: TEC: BITLYFE Digital Companion
- **System**: MCP-enabled AI assistant ecosystem
- **Goal**: Verify end-to-end Copilot functionality

Please assign this issue to @copilot to test the integration.

#github-pull-request_copilot-coding-agent
''',
        "assignees": ["copilot"],
        "labels": ["enhancement", "copilot-test", "mcp-integration"]
    }
    
    # Try to create via GitHub CLI
    try:
        result = subprocess.run([
            'gh', 'issue', 'create',
            '--title', issue_data['title'],
            '--body', issue_data['body'],
            '--assignee', 'copilot',
            '--label', 'enhancement,copilot-test'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ GitHub issue created successfully!")
            print(f"Issue URL: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed to create issue: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ GitHub CLI not found. Install it from: https://cli.github.com/")
        print("Alternative: Create the issue manually on GitHub.com")
        return False

def setup_github_token():
    """Help user set up GitHub token"""
    print("\n🔑 GitHub Token Setup")
    print("=" * 40)
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Select these permissions:")
    print("   ✓ repo (full repository access)")
    print("   ✓ workflow (update workflows)")
    print("   ✓ read:org (read organization data)")
    print("   ✓ models:read (GitHub AI models)")
    print("4. Copy the generated token")
    print("5. Set it in your environment:")
    print("   PowerShell: $env:GITHUB_TOKEN='your-token-here'")
    print("   CMD: set GITHUB_TOKEN=your-token-here")
    print("   .env file: GITHUB_TOKEN=your-token-here")
    
    # Prompt for token
    token = input("\nPaste your GitHub token here (or press Enter to skip): ").strip()
    if token:
        # Update .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Replace or add GitHub token
            lines = content.split('\n')
            token_set = False
            for i, line in enumerate(lines):
                if line.startswith('GITHUB_TOKEN='):
                    lines[i] = f'GITHUB_TOKEN={token}'
                    token_set = True
                    break
            
            if not token_set:
                lines.append(f'GITHUB_TOKEN={token}')
            
            with open(env_file, 'w') as f:
                f.write('\n'.join(lines))
            
            print("✅ GitHub token saved to .env file")
            
            # Set in current environment
            os.environ['GITHUB_TOKEN'] = token
            print("✅ GitHub token set in current session")
            
        else:
            print("❌ .env file not found. Please set the token manually.")

def main():
    """Main diagnostic and resolution workflow"""
    print("TEC GitHub Integration Diagnostic & Resolution Tool")
    print("The Creator's Rebellion - Digital Sovereignty")
    
    # Run diagnostics
    all_good = check_github_setup()
    
    if not all_good:
        print("\n🔧 Would you like to set up your GitHub token? (y/n): ", end="")
        if input().lower().startswith('y'):
            setup_github_token()
            print("\nRe-running diagnostics after token setup...")
            all_good = check_github_setup()
    
    if all_good:
        print("\n🎯 Would you like to create a test issue for Copilot? (y/n): ", end="")
        if input().lower().startswith('y'):
            create_github_issue()
    
    print("\n🎉 GitHub integration diagnostic complete!")
    print("Next steps:")
    print("1. Make sure TEC system is running: python tec_simple_startup.py")
    print("2. Open browser to: http://localhost:8000")
    print("3. Test the web interface")
    print("4. Create GitHub issues and assign to @copilot for AI assistance")

if __name__ == "__main__":
    main()
