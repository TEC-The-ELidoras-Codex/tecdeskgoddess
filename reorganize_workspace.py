#!/usr/bin/env python3
"""
TEC Workspace Reorganization Script
Moves files to the new clean structure
"""
import os
import shutil
from pathlib import Path

class WorkspaceOrganizer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.moves = []
        
    def plan_moves(self):
        """Plan all file moves according to the new structure"""
        
        # Documentation files to docs/
        doc_files = [
            'COMPLETE_STATUS_SUMMARY.md',
            'COPILOT_INTEGRATION.md', 
            'COPILOT_MCP_READY.md',
            'COPILOT_TEST_ISSUE.md',
            'FLASKREADME.md',
            'IMPLEMENTATION_STATUS.md',
            'NEXT_STEPS.md',
            'PHP_INSTALLATION_GUIDE.md',
            'SYSTEM_OPERATIONAL.md',
            'SYSTEM_STATUS.md',
            'TEC_AI_Integration_Guide.ipynb',
            'PROJECT_STRUCTURE_STANDARD.md'
        ]
        
        for file in doc_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'docs/{file}'))
        
        # Test files to tests/ (consolidate)
        test_files = [
            'test_copilot_mcp.py',
            'test_github_ai.py', 
            'test_mcp_system.py',
            'test_tec_system.py',
            'demo_tec_mcp.py',
            'test_request.json'
        ]
        
        for file in test_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'tests/{file}'))
        
        # Scripts to scripts/
        script_files = [
            'setup_tec.py',
            'setup_copilot_ready.py',
            'setup.ps1',
            'tec_startup.py',
            'tec_startup_windows.py',
            'tec_simple_startup.py',
            'start_tec.py',
            'status_check.py',
            'reset_and_test.py',
            'success_report.py',
            'fix_github_issues.py',
            'list_models.py',
            'tec_quickstart.py'
        ]
        
        for file in script_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'scripts/{file}'))
        
        # Config files to config/
        config_files = [
            'config.json',
            '.env.template'
        ]
        
        for file in config_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'config/{file}'))
        
        # Source code to src/
        src_files = [
            'simple_api.py'
        ]
        
        for file in src_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'src/{file}'))
        
        # Move tec_tools to src/
        if (self.base_path / 'tec_tools').exists():
            self.moves.append(('tec_tools', 'src/tec_tools'))
        
        # Integration files to integrations/
        if (self.base_path / 'wordpress').exists():
            self.moves.append(('wordpress', 'integrations/wordpress'))
        
        if (self.base_path / 'ai_modules').exists():
            self.moves.append(('ai_modules', 'integrations/ai_modules'))
        
        # Examples to examples/
        example_files = [
            'tec_chat.html',
            'tec_complete_interface.html'
        ]
        
        for file in example_files:
            if (self.base_path / file).exists():
                self.moves.append((file, f'examples/{file}'))
        
        # Keep in root (important files)
        root_keep = [
            'README.md',
            'requirements.txt',
            'LICENSE',
            '.env',
            '.gitignore',
            'tec_startup.log'  # Current log file
        ]
        
        return self.moves
    
    def execute_moves(self, dry_run=True):
        """Execute the planned moves"""
        print("🧹 TEC Workspace Reorganization Plan")
        print("=" * 50)
        
        for old_path, new_path in self.moves:
            old_full = self.base_path / old_path
            new_full = self.base_path / new_path
            
            if old_full.exists():
                if dry_run:
                    print(f"📁 MOVE: {old_path} → {new_path}")
                else:
                    # Create parent directory if needed
                    new_full.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move the file/directory
                    shutil.move(str(old_full), str(new_full))
                    print(f"✅ MOVED: {old_path} → {new_path}")
            else:
                if dry_run:
                    print(f"⚠️  SKIP: {old_path} (not found)")
        
        if dry_run:
            print("\n" + "=" * 50)
            print("This was a DRY RUN. No files were moved.")
            print("Run with dry_run=False to execute moves.")
        else:
            print("\n🎉 Reorganization complete!")
    
    def create_main_entry_point(self):
        """Create a main.py entry point"""
        main_content = '''#!/usr/bin/env python3
"""
TEC: BITLYFE - Main Entry Point
The Creator's Rebellion - Digital Sovereignty Companion

Usage:
    python main.py              # Start simple web interface
    python main.py --full       # Start full MCP ecosystem
    python main.py --setup      # Run initial setup
    python main.py --status     # Check system status
"""
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    parser = argparse.ArgumentParser(description="TEC: BITLYFE - Digital Sovereignty Companion")
    parser.add_argument('--full', action='store_true', help='Start full MCP ecosystem')
    parser.add_argument('--setup', action='store_true', help='Run initial setup')
    parser.add_argument('--status', action='store_true', help='Check system status')
    parser.add_argument('--simple', action='store_true', help='Start simple web interface (default)')
    
    args = parser.parse_args()
    
    if args.setup:
        from scripts.setup_tec import main as setup_main
        setup_main()
    elif args.status:
        from scripts.status_check import main as status_main
        status_main()
    elif args.full:
        from scripts.tec_startup import main as startup_main
        startup_main()
    else:
        # Default: simple startup
        from scripts.tec_simple_startup import main as simple_main
        simple_main()

if __name__ == "__main__":
    main()
'''
        
        main_file = self.base_path / "main.py"
        with open(main_file, 'w') as f:
            f.write(main_content)
        
        print(f"✅ Created main entry point: {main_file}")

def main():
    base_path = Path(__file__).parent
    organizer = WorkspaceOrganizer(base_path)
    
    # Plan the moves
    moves = organizer.plan_moves()
    
    print(f"Planning to move {len(moves)} items...")
    
    # Show the plan first
    organizer.execute_moves(dry_run=True)
    
    # Ask for confirmation
    response = input("\nExecute this reorganization? (y/N): ").strip().lower()
    
    if response == 'y':
        # Execute the moves
        organizer.execute_moves(dry_run=False)
        
        # Create main entry point
        organizer.create_main_entry_point()
        
        print("\n🎉 Workspace reorganization complete!")
        print("New structure:")
        print("├── src/           # Source code")
        print("├── tests/         # All tests")
        print("├── docs/          # Documentation")
        print("├── scripts/       # Setup/utility scripts")
        print("├── config/        # Configuration")
        print("├── integrations/  # External integrations")
        print("├── examples/      # Examples and demos")
        print("└── main.py        # Main entry point")
        
    else:
        print("Reorganization cancelled.")

if __name__ == "__main__":
    main()
