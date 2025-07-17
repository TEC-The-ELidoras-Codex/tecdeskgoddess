"""
TEC Enhanced Data Persistence Manager
Handles backup, restore, and data migration for cross-platform compatibility
"""

import os
import sqlite3
import json
import shutil
import datetime
import zipfile
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

class TECDataManager:
    def __init__(self, base_path: str = "./data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        self.db_path = self.base_path / "tec_database.db"
        self.backup_path = self.base_path / "backups"
        self.backup_path.mkdir(exist_ok=True)
        
        self.settings_path = self.base_path / "settings.json"
        self.logs_path = self.base_path / "logs"
        self.logs_path.mkdir(exist_ok=True)
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup persistent logging"""
        log_file = self.logs_path / f"tec_data_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TECDataManager')
        
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create a complete system backup"""
        if not backup_name:
            backup_name = f"tec_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_file = self.backup_path / f"{backup_name}.zip"
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup database
                if self.db_path.exists():
                    zipf.write(self.db_path, "tec_database.db")
                
                # Backup settings
                if self.settings_path.exists():
                    zipf.write(self.settings_path, "settings.json")
                
                # Backup conversation history
                conv_path = self.base_path / "conversations"
                if conv_path.exists():
                    for file in conv_path.rglob("*"):
                        if file.is_file():
                            zipf.write(file, file.relative_to(self.base_path))
                
                # Backup user data
                user_data_path = self.base_path / "user_data"
                if user_data_path.exists():
                    for file in user_data_path.rglob("*"):
                        if file.is_file():
                            zipf.write(file, file.relative_to(self.base_path))
            
            self.logger.info(f"Backup created: {backup_file}")
            return str(backup_file)
            
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            raise
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore from backup file"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            self.logger.error(f"Backup file not found: {backup_file}")
            return False
        
        try:
            # Create restore point
            self.create_backup("pre_restore_backup")
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(self.base_path)
            
            self.logger.info(f"Backup restored from: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return False
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save application settings persistently"""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(settings, f, indent=2, default=str)
            
            self.logger.info("Settings saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
            return False
    
    def load_settings(self) -> Dict[str, Any]:
        """Load application settings"""
        if not self.settings_path.exists():
            return self.get_default_settings()
        
        try:
            with open(self.settings_path, 'r') as f:
                settings = json.load(f)
            
            self.logger.info("Settings loaded successfully")
            return settings
            
        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")
            return self.get_default_settings()
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default application settings"""
        return {
            "version": "2.0.0",
            "last_updated": datetime.datetime.now().isoformat(),
            "ai_settings": {
                "creativity": 70,
                "memory": "medium",
                "reasoning": "balanced",
                "mode": "enhanced"
            },
            "audio_settings": {
                "tts_enabled": True,
                "voice_input_enabled": True,
                "character_voices": {
                    "Polkin": {"pitch": 1.2, "rate": 1.1},
                    "Mynx": {"pitch": 0.8, "rate": 0.9},
                    "Kaelen": {"pitch": 1.0, "rate": 1.0}
                }
            },
            "visual_settings": {
                "theme": "default",
                "animations_enabled": True,
                "particles_enabled": True
            },
            "backup_settings": {
                "auto_backup": True,
                "backup_interval": 3600,  # 1 hour
                "max_backups": 10
            }
        }
    
    def save_conversation(self, conversation_id: str, messages: List[Dict]) -> bool:
        """Save conversation history"""
        conv_dir = self.base_path / "conversations"
        conv_dir.mkdir(exist_ok=True)
        
        conv_file = conv_dir / f"{conversation_id}.json"
        
        try:
            conversation_data = {
                "id": conversation_id,
                "created": datetime.datetime.now().isoformat(),
                "messages": messages,
                "message_count": len(messages)
            }
            
            with open(conv_file, 'w') as f:
                json.dump(conversation_data, f, indent=2, default=str)
            
            self.logger.info(f"Conversation saved: {conversation_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save conversation: {e}")
            return False
    
    def load_conversation(self, conversation_id: str) -> Optional[List[Dict]]:
        """Load conversation history"""
        conv_file = self.base_path / "conversations" / f"{conversation_id}.json"
        
        if not conv_file.exists():
            return None
        
        try:
            with open(conv_file, 'r') as f:
                data = json.load(f)
            
            return data.get("messages", [])
            
        except Exception as e:
            self.logger.error(f"Failed to load conversation: {e}")
            return None
    
    def export_data(self, export_path: str) -> bool:
        """Export all data for migration"""
        export_file = Path(export_path)
        
        try:
            export_data = {
                "export_date": datetime.datetime.now().isoformat(),
                "version": "2.0.0",
                "settings": self.load_settings(),
                "database_backup": None,
                "conversations": []
            }
            
            # Export database as base64
            if self.db_path.exists():
                import base64
                with open(self.db_path, 'rb') as f:
                    export_data["database_backup"] = base64.b64encode(f.read()).decode()
            
            # Export conversations
            conv_dir = self.base_path / "conversations"
            if conv_dir.exists():
                for conv_file in conv_dir.glob("*.json"):
                    with open(conv_file, 'r') as f:
                        conv_data = json.load(f)
                        export_data["conversations"].append(conv_data)
            
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Data exported to: {export_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """Import data from migration file"""
        import_file = Path(import_path)
        
        if not import_file.exists():
            self.logger.error(f"Import file not found: {import_path}")
            return False
        
        try:
            with open(import_file, 'r') as f:
                import_data = json.load(f)
            
            # Create backup before import
            self.create_backup("pre_import_backup")
            
            # Import settings
            if "settings" in import_data:
                self.save_settings(import_data["settings"])
            
            # Import database
            if "database_backup" in import_data and import_data["database_backup"]:
                import base64
                db_data = base64.b64decode(import_data["database_backup"])
                with open(self.db_path, 'wb') as f:
                    f.write(db_data)
            
            # Import conversations
            if "conversations" in import_data:
                conv_dir = self.base_path / "conversations"
                conv_dir.mkdir(exist_ok=True)
                
                for conv_data in import_data["conversations"]:
                    conv_file = conv_dir / f"{conv_data['id']}.json"
                    with open(conv_file, 'w') as f:
                        json.dump(conv_data, f, indent=2)
            
            self.logger.info(f"Data imported from: {import_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            return False
    
    def cleanup_old_backups(self, max_backups: int = 10):
        """Clean up old backup files"""
        backups = list(self.backup_path.glob("*.zip"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if len(backups) > max_backups:
            for backup in backups[max_backups:]:
                try:
                    backup.unlink()
                    self.logger.info(f"Deleted old backup: {backup}")
                except Exception as e:
                    self.logger.error(f"Failed to delete backup {backup}: {e}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = {
            "database_size": 0,
            "conversations_count": 0,
            "backups_count": 0,
            "total_data_size": 0,
            "last_backup": None
        }
        
        try:
            # Database size
            if self.db_path.exists():
                stats["database_size"] = self.db_path.stat().st_size
            
            # Conversations count
            conv_dir = self.base_path / "conversations"
            if conv_dir.exists():
                stats["conversations_count"] = len(list(conv_dir.glob("*.json")))
            
            # Backups count and last backup
            backups = list(self.backup_path.glob("*.zip"))
            stats["backups_count"] = len(backups)
            
            if backups:
                latest_backup = max(backups, key=lambda x: x.stat().st_mtime)
                stats["last_backup"] = datetime.datetime.fromtimestamp(
                    latest_backup.stat().st_mtime
                ).isoformat()
            
            # Total data size
            total_size = 0
            for file in self.base_path.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size
            stats["total_data_size"] = total_size
            
        except Exception as e:
            self.logger.error(f"Failed to get system stats: {e}")
        
        return stats

# Data manager instance
data_manager = TECDataManager()

def create_backup():
    """CLI function to create backup"""
    return data_manager.create_backup()

def restore_backup(backup_file: str):
    """CLI function to restore backup"""
    return data_manager.restore_backup(backup_file)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_persistence.py [backup|restore|export|import|stats] [file]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "backup":
        backup_file = data_manager.create_backup()
        print(f"Backup created: {backup_file}")
    
    elif command == "restore" and len(sys.argv) > 2:
        success = data_manager.restore_backup(sys.argv[2])
        print(f"Restore {'successful' if success else 'failed'}")
    
    elif command == "export" and len(sys.argv) > 2:
        success = data_manager.export_data(sys.argv[2])
        print(f"Export {'successful' if success else 'failed'}")
    
    elif command == "import" and len(sys.argv) > 2:
        success = data_manager.import_data(sys.argv[2])
        print(f"Import {'successful' if success else 'failed'}")
    
    elif command == "stats":
        stats = data_manager.get_system_stats()
        print("System Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print("Invalid command or missing arguments")
        sys.exit(1)
