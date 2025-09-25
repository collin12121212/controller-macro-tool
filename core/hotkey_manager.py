"""
Global Hotkey Manager for Controller Macro Tool
Provides global keyboard shortcuts that work even when the app is minimized
"""

import threading
import time
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

class HotkeyManager:
    def __init__(self):
        self.hotkeys = {}
        self.listener = None
        self.running = False
        self.pressed_keys = set()
        
        # Default hotkey mappings
        self.default_hotkeys = {
            'start_stop_recording': {Key.ctrl_l, KeyCode.from_char('r')},
            'play_last_macro': {Key.ctrl_l, KeyCode.from_char('p')},
            'stop_all': {Key.ctrl_l, KeyCode.from_char('s')},
            'quick_record': {Key.f9},
            'emergency_stop': {Key.f10},
        }
        
        # Initialize with defaults
        self.hotkeys = self.default_hotkeys.copy()
        
        # Callback functions
        self.callbacks = {}
        
    def set_hotkey(self, action, keys):
        """Set a hotkey for a specific action"""
        if isinstance(keys, (str, KeyCode, Key)):
            keys = {keys}
        elif isinstance(keys, (list, tuple)):
            keys = set(keys)
        
        self.hotkeys[action] = keys
        
    def register_callback(self, action, callback):
        """Register a callback function for a hotkey action"""
        self.callbacks[action] = callback
        
    def start_monitoring(self):
        """Start monitoring for global hotkeys"""
        if self.running:
            return
            
        self.running = True
        
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.listener.start()
            print("Global hotkey monitoring started")
        except Exception as e:
            print(f"Failed to start hotkey monitoring: {e}")
            self.running = False
            
    def stop_monitoring(self):
        """Stop monitoring for global hotkeys"""
        if not self.running:
            return
            
        self.running = False
        
        if self.listener:
            try:
                self.listener.stop()
                self.listener = None
                print("Global hotkey monitoring stopped")
            except Exception as e:
                print(f"Error stopping hotkey listener: {e}")
                
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            self.pressed_keys.add(key)
            self._check_hotkey_combinations()
        except Exception as e:
            print(f"Error in key press handler: {e}")
            
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            self.pressed_keys.discard(key)
        except Exception as e:
            print(f"Error in key release handler: {e}")
            
    def _check_hotkey_combinations(self):
        """Check if any hotkey combinations are currently pressed"""
        for action, hotkey_combo in self.hotkeys.items():
            if hotkey_combo.issubset(self.pressed_keys):
                self._trigger_hotkey(action)
                
    def _trigger_hotkey(self, action):
        """Trigger a hotkey action"""
        callback = self.callbacks.get(action)
        if callback:
            try:
                # Run callback in a separate thread to avoid blocking
                thread = threading.Thread(target=callback, daemon=True)
                thread.start()
                print(f"Triggered hotkey action: {action}")
            except Exception as e:
                print(f"Error executing hotkey callback for {action}: {e}")
                
    def get_hotkey_string(self, action):
        """Get a human-readable string for a hotkey"""
        hotkey_combo = self.hotkeys.get(action, set())
        if not hotkey_combo:
            return "Not set"
            
        key_names = []
        for key in hotkey_combo:
            if hasattr(key, 'name'):
                if key == Key.ctrl_l or key == Key.ctrl_r:
                    key_names.append('Ctrl')
                elif key == Key.shift_l or key == Key.shift_r:
                    key_names.append('Shift')
                elif key == Key.alt_l or key == Key.alt_r:
                    key_names.append('Alt')
                else:
                    key_names.append(key.name.title())
            elif hasattr(key, 'char') and key.char:
                key_names.append(key.char.upper())
            else:
                key_names.append(str(key))
                
        return ' + '.join(sorted(key_names))
        
    def get_all_hotkeys(self):
        """Get all configured hotkeys with their string representations"""
        return {action: self.get_hotkey_string(action) for action in self.hotkeys}
        
    def parse_hotkey_string(self, hotkey_string):
        """Parse a hotkey string into key objects"""
        if not hotkey_string or hotkey_string == "Not set":
            return set()
            
        keys = set()
        parts = [part.strip() for part in hotkey_string.split('+')]
        
        for part in parts:
            part_lower = part.lower()
            if part_lower == 'ctrl':
                keys.add(Key.ctrl_l)
            elif part_lower == 'shift':
                keys.add(Key.shift_l)
            elif part_lower == 'alt':
                keys.add(Key.alt_l)
            elif part_lower.startswith('f') and part_lower[1:].isdigit():
                # Function keys
                func_num = int(part_lower[1:])
                if 1 <= func_num <= 12:
                    keys.add(getattr(Key, f'f{func_num}'))
            elif len(part) == 1:
                keys.add(KeyCode.from_char(part.lower()))
            else:
                # Try to get special keys
                try:
                    keys.add(getattr(Key, part_lower))
                except AttributeError:
                    print(f"Unknown key: {part}")
                    
        return keys
        
    def is_running(self):
        """Check if hotkey monitoring is running"""
        return self.running and self.listener and self.listener.running