# 🎯 TEC Project Structure Template

## 📁 Standard Folder Structure

```
project_name/
├── 📂 src/                    # 🎯 Main source code
│   ├── __init__.py           # Package initialization
│   ├── main_module.py        # Core functionality
│   ├── api/                  # API endpoints
│   ├── models/               # Data models
│   ├── utils/                # Utility functions
│   └── integrations/         # Internal integrations
│
├── 📂 tests/                  # 🧪 All test files
│   ├── __init__.py           # Test package init
│   ├── test_main.py          # Main functionality tests
│   ├── test_api.py           # API tests
│   ├── integration/          # Integration tests
│   ├── unit/                 # Unit tests
│   ├── fixtures/             # Test data
│   └── conftest.py           # Pytest configuration
│
├── 📂 docs/                   # 📚 Documentation
│   ├── README.md             # Main documentation
│   ├── INSTALLATION.md       # Setup instructions
│   ├── API.md                # API documentation
│   ├── CHANGELOG.md          # Version history
│   ├── CONTRIBUTING.md       # Contribution guide
│   └── architecture.md       # System architecture
│
├── 📂 scripts/                # ⚙️ Utility scripts
│   ├── setup.py              # Initial setup
│   ├── deploy.py             # Deployment
│   ├── backup.py             # Data backup
│   ├── migrate.py            # Data migration
│   └── cleanup.py            # Maintenance
│
├── 📂 config/                 # ⚙️ Configuration files
│   ├── .env.template         # Environment template
│   ├── settings.json         # App settings
│   ├── database.conf         # Database config
│   └── logging.conf          # Logging config
│
├── 📂 integrations/           # 🔌 External integrations
│   ├── wordpress/            # WordPress plugin
│   ├── github/               # GitHub integration
│   ├── azure/                # Azure services
│   └── ai_providers/         # AI service integrations
│
├── 📂 examples/               # 💡 Examples and demos
│   ├── basic_usage.py        # Basic example
│   ├── advanced_demo.py      # Advanced features
│   ├── web_interface.html    # Web examples
│   └── tutorials/            # Step-by-step guides
│
├── 📂 assets/                 # 📁 Static assets
│   ├── images/               # Image files
│   ├── audio/                # Audio files
│   ├── fonts/                # Font files
│   └── icons/                # Icon files
│
├── 📂 data/                   # 📊 Data files (auto-generated)
│   ├── cache/                # Cache files
│   ├── temp/                 # Temporary files
│   └── exports/              # Exported data
│
├── 📂 logs/                   # 📝 Log files (auto-generated)
│   ├── app.log               # Application logs
│   ├── error.log             # Error logs
│   └── access.log            # Access logs
│
├── 📂 archive/                # 📦 Old/deprecated files
│   ├── old_versions/         # Previous versions
│   ├── experimental/         # Experimental code
│   └── deprecated/           # Deprecated features
│
└── 📄 Root Files:
    ├── main.py               # 🚀 Main entry point
    ├── README.md             # 📖 Project overview
    ├── requirements.txt      # 📦 Python dependencies
    ├── .env                  # 🔐 Environment variables
    ├── .gitignore           # 🚫 Git ignore rules
    ├── LICENSE              # ⚖️ License file
    └── pyproject.toml       # 🛠️ Python project config
```

## 🎨 Naming Conventions

### Files:
- **Python**: `snake_case.py`
- **Config**: `kebab-case.json`
- **Docs**: `UPPERCASE.md` for important docs, `lowercase.md` for others
- **Scripts**: `descriptive_action.py`

### Folders:
- **Lowercase**: All folder names
- **Plural**: For collections (tests, docs, scripts, examples)
- **Singular**: For single purpose (config, data, src)
- **Descriptive**: Clear purpose (integrations, assets, archive)

### Code:
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Variables**: `snake_case`

## 🔧 Setup Commands

### Create New Project:
```bash
mkdir project_name && cd project_name
mkdir src tests docs scripts config integrations examples assets data logs archive
touch main.py README.md requirements.txt .env .gitignore LICENSE
```

### Initialize Files:
```bash
echo "# Project Name" > README.md
echo "# Requirements" > requirements.txt
echo "*.pyc\n__pycache__/\n.env\ndata/\nlogs/" > .gitignore
```

## 📋 Project Checklist

### Initial Setup:
- [ ] Create folder structure
- [ ] Set up main.py entry point
- [ ] Write README.md
- [ ] Configure .gitignore
- [ ] Set up requirements.txt
- [ ] Create .env.template

### Development:
- [ ] Add src/ modules
- [ ] Write tests in tests/
- [ ] Document in docs/
- [ ] Create utility scripts/
- [ ] Add examples/

### Finalization:
- [ ] Update CHANGELOG.md
- [ ] Clean up archive/
- [ ] Verify all tests pass
- [ ] Update documentation
- [ ] Tag version

## 🎯 Benefits of This Structure:

1. **🧹 Clean Root**: Only essential files in root directory
2. **🔍 Easy Navigation**: Find any file type quickly
3. **📦 Scalable**: Works for small and large projects
4. **🤝 Team Friendly**: Clear conventions for collaboration
5. **🚀 Professional**: Industry-standard organization
6. **🔄 Reusable**: Template for all future projects

## 💾 Template Generation Script:

```python
import os
from pathlib import Path

def create_project_template(project_name):
    folders = [
        'src', 'tests', 'docs', 'scripts', 'config',
        'integrations', 'examples', 'assets', 'data', 'logs', 'archive'
    ]
    
    Path(project_name).mkdir(exist_ok=True)
    os.chdir(project_name)
    
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        
    # Create essential files
    files = {
        'main.py': '#!/usr/bin/env python3\n"""Main entry point"""\n\nif __name__ == "__main__":\n    print("Hello World!")',
        'README.md': f'# {project_name}\n\nProject description here.',
        'requirements.txt': '# Python dependencies\n',
        '.gitignore': '*.pyc\n__pycache__/\n.env\ndata/\nlogs/\nvenv/',
        '.env.template': '# Environment variables template\nAPI_KEY=your_api_key_here'
    }
    
    for filename, content in files.items():
        with open(filename, 'w') as f:
            f.write(content)
    
    print(f"✅ Created project template: {project_name}")

# Usage: create_project_template("my_new_project")
```

## 🚀 Remember This Structure!

Save this template for all future TEC projects. It ensures:
- Consistent organization across projects
- Easy onboarding for new team members
- Professional project presentation
- Scalable architecture from day one

**This is our TEC Standard - use it for every project!**
