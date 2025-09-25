#!/usr/bin/env python3
"""
Comprehensive functionality test for Controller Macro Tool
Tests all major components without requiring GUI or controllers
"""

import sys
import os
import json
import tempfile
import time
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_theme_manager():
    """Test theme manager functionality"""
    print("Testing ThemeManager...")
    
    try:
        from gui.theme_manager import ThemeManager
        theme = ThemeManager()
        
        # Test color access
        assert theme.get_color('bg_primary') == '#1a1a1a'
        assert theme.get_color('accent_blue') == '#0078d4'
        
        # Test font access
        font = theme.get_font('default')
        assert isinstance(font, tuple)
        assert len(font) >= 2
        
        print("✓ ThemeManager tests passed")
        return True
    except Exception as e:
        print(f"✗ ThemeManager test failed: {e}")
        return False

def test_hotkey_manager():
    """Test hotkey manager functionality"""
    print("Testing HotkeyManager...")
    
    try:
        from core.hotkey_manager import HotkeyManager
        hotkey_manager = HotkeyManager()
        
        # Test hotkey string parsing
        keys = hotkey_manager.parse_hotkey_string("Ctrl + R")
        assert len(keys) == 2
        
        # Test hotkey string generation
        hotkey_str = hotkey_manager.get_hotkey_string('start_stop_recording')
        assert isinstance(hotkey_str, str)
        assert len(hotkey_str) > 0
        
        # Test callback registration
        callback_called = False
        def test_callback():
            nonlocal callback_called
            callback_called = True
            
        hotkey_manager.register_callback('test_action', test_callback)
        assert 'test_action' in hotkey_manager.callbacks
        
        print("✓ HotkeyManager tests passed")
        return True
    except Exception as e:
        print(f"✗ HotkeyManager test failed: {e}")
        return False

def test_macro_manager():
    """Test advanced macro manager functionality"""
    print("Testing MacroManager...")
    
    try:
        from core.macro_manager import MacroManager, MacroType
        manager = MacroManager()
        
        # Test macro addition
        test_macro = [
            {'type': 'button', 'timestamp': 0.0, 'button': 'A', 'value': True, 'duration': 0},
            {'type': 'button', 'timestamp': 0.1, 'button': 'A', 'value': False, 'duration': 0}
        ]
        
        success = manager.add_macro("test_macro", test_macro, description="Test macro")
        assert success
        assert "test_macro" in manager.macros
        
        # Test metadata
        metadata = manager.get_metadata("test_macro")
        assert metadata is not None
        assert metadata.name == "test_macro"
        assert metadata.input_count == 2
        
        # Test macro search
        results = manager.search_macros("test")
        assert "test_macro" in results
        
        # Test favorites
        is_favorite = manager.toggle_favorite("test_macro")
        assert is_favorite
        assert "test_macro" in manager.get_favorites()
        
        # Test macro chain creation
        manager.add_macro("macro2", test_macro)
        chain_success = manager.create_macro_chain("test_chain", ["test_macro", "macro2"])
        assert chain_success
        assert "test_chain" in manager.macros
        
        # Test statistics
        stats = manager.get_macro_statistics()
        assert stats['total_macros'] >= 3
        assert isinstance(stats['type_distribution'], dict)
        
        print("✓ MacroManager tests passed")
        return True
    except Exception as e:
        print(f"✗ MacroManager test failed: {e}")
        return False

def test_macro_player():
    """Test macro player functionality"""
    print("Testing MacroPlayer...")
    
    try:
        # Mock controller manager
        mock_controller = Mock()
        
        from core.macro_player import MacroPlayer
        player = MacroPlayer(mock_controller)
        
        # Test key mappings
        assert 'A' in player.key_mappings
        assert player.key_mappings['A'] == 'space'
        
        # Test empty macro handling
        result = player.play_macro([])
        assert result == False
        
        # Test concurrent playback prevention
        player.playing = True
        result = player.play_macro([{'type': 'button', 'timestamp': 0, 'button': 'A', 'value': True}])
        assert result == False
        player.playing = False
        
        print("✓ MacroPlayer tests passed")
        return True
    except Exception as e:
        print(f"✗ MacroPlayer test failed: {e}")
        return False

def test_config_manager():
    """Test configuration manager"""
    print("Testing ConfigManager...")
    
    try:
        from core.config_manager import ConfigManager
        config = ConfigManager()
        
        # Test setting management
        config.set_setting('test_key', 'test_value')
        assert config.get_setting('test_key') == 'test_value'
        assert config.get_setting('nonexistent', 'default') == 'default'
        
        # Test macro save/load with temporary file
        test_macros = {
            'test_macro': [
                {'type': 'button', 'timestamp': 0, 'button': 'A', 'value': True}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            
        try:
            # Test save
            success = config.save_macros(test_macros, temp_file)
            assert success
            assert os.path.exists(temp_file)
            
            # Test load
            loaded_macros = config.load_macros(temp_file)
            assert isinstance(loaded_macros, dict)
            assert 'test_macro' in loaded_macros
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        print("✓ ConfigManager tests passed")
        return True
    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        return False

def test_notification_system():
    """Test notification system without GUI"""
    print("Testing NotificationManager...")
    
    try:
        # Since we can't test GUI without display, we'll test the logic
        from gui.notification_manager import StatusManager
        
        # Mock status label
        mock_label = Mock()
        mock_theme = Mock()
        mock_theme.get_color.return_value = '#ffffff'
        
        status_manager = StatusManager(mock_label, mock_theme)
        
        # Test status updates
        status_manager.update_status("Test status", "info")
        assert status_manager.get_current_status() == "Test status"
        
        # Test flash status (async operation)
        original_status = status_manager.get_current_status()
        status_manager.flash_status("Flash message", "warning", 100)  # Short duration
        time.sleep(0.2)  # Wait for flash to complete
        
        print("✓ NotificationManager tests passed")
        return True
    except Exception as e:
        print(f"✗ NotificationManager test failed: {e}")
        return False

def run_all_tests():
    """Run all functionality tests"""
    print("=" * 60)
    print("Controller Macro Tool - Comprehensive Functionality Test")
    print("=" * 60)
    
    tests = [
        test_theme_manager,
        test_hotkey_manager,
        test_macro_manager,
        test_macro_player,
        test_config_manager,
        test_notification_system,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The application is ready.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)