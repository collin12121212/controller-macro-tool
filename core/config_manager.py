"""
Configuration and data management
"""

import json
import os
from datetime import datetime

class ConfigManager:
    def __init__(self):
        self.config_dir = "config"
        self.macros_dir = "macros"
        self.config_file = "settings.json"
        
        self.ensure_directories()
        self.default_settings = {
            'theme': 'dark',
            'auto_save': True,
            'recording_quality': 'high',
            'default_key_mappings': {
                'A': 'space',
                'B': 'x',
                'X': 'z',
                'Y': 'c'
            },
            'window_geometry': '1200x800',
            'last_macro_directory': self.macros_dir
        }
        
        self.settings = self.load_settings()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [self.config_dir, self.macros_dir]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def load_settings(self):
        """Load application settings"""
        settings_path = os.path.join(self.config_dir, self.config_file)
        
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    
                # Merge with defaults
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                return settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            
        return self.default_settings.copy()
        
    def save_settings(self):
        """Save current settings to file"""
        settings_path = os.path.join(self.config_dir, self.config_file)
        
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
            
    def get_setting(self, key, default=None):
        """Get a specific setting value"""
        return self.settings.get(key, default)
        
    def set_setting(self, key, value):
        """Set a specific setting value"""
        self.settings[key] = value
        
    def save_macros(self, macros, file_path=None):
        """Save macros to file"""
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(self.macros_dir, f"macros_{timestamp}.json")
            
        try:
            # Prepare data for saving
            save_data = {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'macros': macros
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error saving macros: {e}")
            return False
            
    def load_macros(self, file_path):
        """Load macros from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle different file formats
            if isinstance(data, dict) and 'macros' in data:
                return data['macros']
            elif isinstance(data, dict):
                # Assume it's a direct macro dictionary
                return data
            else:
                return {}
                
        except Exception as e:
            print(f"Error loading macros: {e}")
            return {}
            
    def get_recent_macro_files(self, limit=10):
        """Get list of recent macro files"""
        try:
            macro_files = []
            for filename in os.listdir(self.macros_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.macros_dir, filename)
                    stat = os.stat(file_path)
                    macro_files.append({
                        'name': filename,
                        'path': file_path,
                        'modified': stat.st_mtime,
                        'size': stat.st_size
                    })
                    
            # Sort by modification time (newest first)
            macro_files.sort(key=lambda x