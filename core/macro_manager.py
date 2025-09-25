"""
Advanced Macro Management System
Handles macro organization, validation, chaining, and advanced features
"""

import json
import time
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class MacroType(Enum):
    SIMPLE = "simple"
    CHAIN = "chain"
    CONDITIONAL = "conditional"
    LOOP = "loop"

@dataclass
class MacroMetadata:
    name: str
    description: str = ""
    tags: List[str] = None
    created_at: float = None
    modified_at: float = None
    usage_count: int = 0
    last_used: float = None
    duration: float = 0.0
    input_count: int = 0
    macro_type: MacroType = MacroType.SIMPLE
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = time.time()
        if self.modified_at is None:
            self.modified_at = self.created_at

class MacroManager:
    def __init__(self):
        self.macros: Dict[str, List[Dict]] = {}
        self.metadata: Dict[str, MacroMetadata] = {}
        self.categories: List[str] = ["General", "Gaming", "Productivity", "Custom"]
        self.favorites: List[str] = []
        
    def add_macro(self, name: str, macro_data: List[Dict], **kwargs) -> bool:
        """Add a new macro with metadata"""
        try:
            # Validate macro data
            if not self.validate_macro(macro_data):
                return False
                
            # Calculate metadata
            duration = self.calculate_duration(macro_data)
            input_count = len(macro_data)
            
            # Create metadata
            metadata = MacroMetadata(
                name=name,
                description=kwargs.get('description', ''),
                tags=kwargs.get('tags', []),
                duration=duration,
                input_count=input_count,
                macro_type=kwargs.get('macro_type', MacroType.SIMPLE)
            )
            
            # Store macro and metadata
            self.macros[name] = macro_data
            self.metadata[name] = metadata
            
            return True
            
        except Exception as e:
            print(f"Error adding macro {name}: {e}")
            return False
            
    def update_macro(self, name: str, macro_data: List[Dict], **kwargs) -> bool:
        """Update an existing macro"""
        if name not in self.macros:
            return False
            
        try:
            # Validate new data
            if not self.validate_macro(macro_data):
                return False
                
            # Update macro data
            self.macros[name] = macro_data
            
            # Update metadata
            metadata = self.metadata[name]
            metadata.modified_at = time.time()
            metadata.duration = self.calculate_duration(macro_data)
            metadata.input_count = len(macro_data)
            
            # Update optional fields
            if 'description' in kwargs:
                metadata.description = kwargs['description']
            if 'tags' in kwargs:
                metadata.tags = kwargs['tags']
                
            return True
            
        except Exception as e:
            print(f"Error updating macro {name}: {e}")
            return False
            
    def delete_macro(self, name: str) -> bool:
        """Delete a macro"""
        if name in self.macros:
            del self.macros[name]
            if name in self.metadata:
                del self.metadata[name]
            if name in self.favorites:
                self.favorites.remove(name)
            return True
        return False
        
    def get_macro(self, name: str) -> Optional[List[Dict]]:
        """Get macro data by name"""
        return self.macros.get(name)
        
    def get_metadata(self, name: str) -> Optional[MacroMetadata]:
        """Get macro metadata by name"""
        return self.metadata.get(name)
        
    def list_macros(self, category: str = None, tag: str = None) -> List[str]:
        """List macros with optional filtering"""
        macro_names = list(self.macros.keys())
        
        if tag:
            macro_names = [name for name in macro_names 
                          if tag in self.metadata.get(name, MacroMetadata(name)).tags]
        
        return sorted(macro_names)
        
    def search_macros(self, query: str) -> List[str]:
        """Search macros by name, description, or tags"""
        query = query.lower()
        results = []
        
        for name, metadata in self.metadata.items():
            # Search in name
            if query in name.lower():
                results.append(name)
                continue
                
            # Search in description
            if query in metadata.description.lower():
                results.append(name)
                continue
                
            # Search in tags
            if any(query in tag.lower() for tag in metadata.tags):
                results.append(name)
                continue
                
        return sorted(results)
        
    def get_recent_macros(self, limit: int = 10) -> List[str]:
        """Get recently used macros"""
        sorted_macros = sorted(
            self.metadata.items(),
            key=lambda x: x[1].last_used or 0,
            reverse=True
        )
        return [name for name, _ in sorted_macros[:limit] if name in self.macros]
        
    def get_popular_macros(self, limit: int = 10) -> List[str]:
        """Get most frequently used macros"""
        sorted_macros = sorted(
            self.metadata.items(),
            key=lambda x: x[1].usage_count,
            reverse=True
        )
        return [name for name, _ in sorted_macros[:limit] if name in self.macros]
        
    def mark_macro_used(self, name: str):
        """Mark a macro as used (for statistics)"""
        if name in self.metadata:
            metadata = self.metadata[name]
            metadata.usage_count += 1
            metadata.last_used = time.time()
            
    def toggle_favorite(self, name: str) -> bool:
        """Toggle macro favorite status"""
        if name not in self.macros:
            return False
            
        if name in self.favorites:
            self.favorites.remove(name)
            return False
        else:
            self.favorites.append(name)
            return True
            
    def get_favorites(self) -> List[str]:
        """Get favorite macros"""
        return [name for name in self.favorites if name in self.macros]
        
    def create_macro_chain(self, name: str, macro_names: List[str], delays: List[float] = None) -> bool:
        """Create a macro chain from existing macros"""
        if delays is None:
            delays = [0.5] * (len(macro_names) - 1)
            
        # Validate all macros exist
        for macro_name in macro_names:
            if macro_name not in self.macros:
                return False
                
        # Create chain data
        chain_data = []
        for i, macro_name in enumerate(macro_names):
            # Add macro events
            macro_events = self.macros[macro_name]
            chain_data.extend(macro_events)
            
            # Add delay between macros (except after last)
            if i < len(macro_names) - 1:
                chain_data.append({
                    'type': 'delay',
                    'timestamp': 0,
                    'button': 'delay',
                    'value': delays[i] * 1000,  # Convert to milliseconds
                    'duration': 0
                })
        
        # Add chain macro
        return self.add_macro(
            name, 
            chain_data,
            description=f"Chain of: {', '.join(macro_names)}",
            tags=['chain', 'composite'],
            macro_type=MacroType.CHAIN
        )
        
    def validate_macro(self, macro_data: List[Dict]) -> bool:
        """Validate macro data structure"""
        if not isinstance(macro_data, list):
            return False
            
        required_fields = ['type', 'timestamp', 'button', 'value']
        
        for event in macro_data:
            if not isinstance(event, dict):
                return False
            for field in required_fields:
                if field not in event:
                    return False
                    
        return True
        
    def calculate_duration(self, macro_data: List[Dict]) -> float:
        """Calculate macro duration in seconds"""
        if not macro_data:
            return 0.0
            
        timestamps = [event.get('timestamp', 0) for event in macro_data]
        return max(timestamps) if timestamps else 0.0
        
    def optimize_macro(self, name: str) -> bool:
        """Optimize a macro by removing redundant events"""
        if name not in self.macros:
            return False
            
        macro_data = self.macros[name]
        optimized_data = []
        last_button_state = {}
        
        for event in macro_data:
            button = event.get('button')
            value = event.get('value')
            event_type = event.get('type')
            
            # Skip redundant button events
            if event_type in ['button', 'dpad']:
                last_state = last_button_state.get(button)
                if last_state == value:
                    continue  # Skip redundant event
                last_button_state[button] = value
                
            optimized_data.append(event)
            
        # Update if optimization made changes
        if len(optimized_data) != len(macro_data):
            self.macros[name] = optimized_data
            self.metadata[name].input_count = len(optimized_data)
            self.metadata[name].modified_at = time.time()
            return True
            
        return False
        
    def get_macro_statistics(self) -> Dict[str, Any]:
        """Get overall macro statistics"""
        total_macros = len(self.macros)
        total_usage = sum(meta.usage_count for meta in self.metadata.values())
        avg_duration = sum(meta.duration for meta in self.metadata.values()) / max(total_macros, 1)
        
        # Macro type distribution
        type_counts = {}
        for meta in self.metadata.values():
            macro_type = meta.macro_type.value
            type_counts[macro_type] = type_counts.get(macro_type, 0) + 1
            
        return {
            'total_macros': total_macros,
            'total_usage': total_usage,
            'average_duration': avg_duration,
            'favorites_count': len(self.favorites),
            'type_distribution': type_counts,
            'most_used': self.get_popular_macros(5),
            'recently_used': self.get_recent_macros(5)
        }
        
    def export_macros(self, file_path: str, macro_names: List[str] = None) -> bool:
        """Export macros to file"""
        try:
            if macro_names is None:
                macro_names = list(self.macros.keys())
                
            export_data = {
                'version': '2.0',
                'exported_at': time.time(),
                'macros': {},
                'metadata': {},
                'favorites': [name for name in self.favorites if name in macro_names]
            }
            
            for name in macro_names:
                if name in self.macros:
                    export_data['macros'][name] = self.macros[name]
                    export_data['metadata'][name] = {
                        'name': self.metadata[name].name,
                        'description': self.metadata[name].description,
                        'tags': self.metadata[name].tags,
                        'created_at': self.metadata[name].created_at,
                        'modified_at': self.metadata[name].modified_at,
                        'usage_count': self.metadata[name].usage_count,
                        'last_used': self.metadata[name].last_used,
                        'duration': self.metadata[name].duration,
                        'input_count': self.metadata[name].input_count,
                        'macro_type': self.metadata[name].macro_type.value
                    }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error exporting macros: {e}")
            return False
            
    def import_macros(self, file_path: str, overwrite: bool = False) -> int:
        """Import macros from file"""
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
                
            imported_count = 0
            
            # Import macros
            macros_data = import_data.get('macros', {})
            metadata_data = import_data.get('metadata', {})
            
            for name, macro_data in macros_data.items():
                if name in self.macros and not overwrite:
                    continue
                    
                # Import macro
                self.macros[name] = macro_data
                
                # Import metadata if available
                if name in metadata_data:
                    meta_dict = metadata_data[name]
                    self.metadata[name] = MacroMetadata(
                        name=meta_dict['name'],
                        description=meta_dict.get('description', ''),
                        tags=meta_dict.get('tags', []),
                        created_at=meta_dict.get('created_at', time.time()),
                        modified_at=meta_dict.get('modified_at', time.time()),
                        usage_count=meta_dict.get('usage_count', 0),
                        last_used=meta_dict.get('last_used'),
                        duration=meta_dict.get('duration', 0.0),
                        input_count=meta_dict.get('input_count', len(macro_data)),
                        macro_type=MacroType(meta_dict.get('macro_type', 'simple'))
                    )
                else:
                    # Create basic metadata
                    self.metadata[name] = MacroMetadata(
                        name=name,
                        duration=self.calculate_duration(macro_data),
                        input_count=len(macro_data)
                    )
                    
                imported_count += 1
                
            # Import favorites
            imported_favorites = import_data.get('favorites', [])
            for name in imported_favorites:
                if name in self.macros and name not in self.favorites:
                    self.favorites.append(name)
                    
            return imported_count
            
        except Exception as e:
            print(f"Error importing macros: {e}")
            return 0