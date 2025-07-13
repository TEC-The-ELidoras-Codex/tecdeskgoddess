# TEC Project Structure Standard

## 🎯 Preferred Project Organization

### Core Structure:
```
project_root/
├── 📁 src/                 # Source code (main application)
├── 📁 tests/               # All test files
├── 📁 docs/                # Documentation files
├── 📁 scripts/             # Setup/utility scripts
├── 📁 config/              # Configuration files
├── 📁 assets/              # Media/static files
├── 📁 data/                # Data files (auto-generated)
├── 📁 logs/                # Log files (auto-generated)
├── 📁 integrations/        # External integrations
├── 📁 examples/            # Example files and demos
└── 📁 archive/             # Old/temporary files
```

### Root Files:
```
├── README.md               # Main project documentation
├── requirements.txt        # Python dependencies
├── .env.template          # Environment template
├── .gitignore             # Git ignore rules
├── LICENSE                # License file
└── main.py                # Main entry point
```

### Development Files:
```
├── 📁 .github/            # GitHub workflows, templates
├── 📁 .vscode/            # VS Code settings
└── 📁 .azure/             # Azure configurations
```

## 🧹 Cleanup Rules:

### Move to tests/:
- All files starting with `test_`
- Test configuration files
- Test data files

### Move to docs/:
- README files (except main)
- Markdown documentation
- Integration guides
- Status reports

### Move to scripts/:
- Setup scripts
- Utility scripts
- One-time use scripts

### Move to config/:
- Configuration JSON files
- Template files
- Environment setups

### Move to archive/:
- Old versions
- Experimental files
- Deprecated scripts

## 🎨 Future Project Template:

When starting new projects, use this structure:
1. Create core folders first
2. Place files in appropriate locations
3. Keep root directory minimal
4. Use clear naming conventions

## 📝 Naming Conventions:

### Files:
- `snake_case` for Python files
- `kebab-case` for config files
- `PascalCase` for classes
- Clear, descriptive names

### Folders:
- Lowercase, descriptive
- Plural for collections (tests, docs, scripts)
- Singular for single purpose (config, data)

## 🚀 Benefits:

1. **Easy Navigation**: Find files quickly
2. **Clear Purpose**: Each folder has specific role
3. **Scalable**: Works for small and large projects
4. **Standard**: Consistent across all projects
5. **Clean**: Root directory stays organized

This structure will be our standard for all future TEC projects!
