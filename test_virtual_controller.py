#!/usr/bin/env python3
"""
Virtual Controller Test Script for Controller Macro Tool
Run this script to test virtual controller functionality on your system.
"""

import sys
import os
import platform
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_virtual_controller():
    """Test virtual controller initialization and basic functionality"""
    print("=" * 60)
    print("Controller Macro Tool - Virtual Controller Test")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    
    try:
        from core.macro_player import MacroPlayer
        from unittest.mock import Mock
        
        # Create mock controller manager
        controller_manager = Mock()
        
        # Initialize macro player
        print("\nInitializing MacroPlayer...")
        mp = MacroPlayer(controller_manager)
        
        # Check virtual controller status
        print(f"\nPlayback Method: {mp.get_playback_method()}")
        
        status = mp.check_virtual_controller_status()
        print(f"\nVirtual Controller Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        # Test a simple macro if virtual controller is working
        if status.get('working', False):
            print("\n✓ Virtual controller is working! Testing macro playback...")
            
            test_macro = [
                {'type': 'button', 'button': 'A', 'value': True, 'timestamp': 0},
                {'type': 'delay', 'value': 100, 'timestamp': 100},
                {'type': 'button', 'button': 'A', 'value': False, 'timestamp': 200},
                {'type': 'trigger', 'button': 'RT', 'value': 0.8, 'timestamp': 300},
                {'type': 'trigger', 'button': 'RT', 'value': 0.0, 'timestamp': 400},
            ]
            
            success = mp.play_macro(test_macro)
            if success:
                print("  ✓ Test macro started successfully")
                time.sleep(1)  # Wait for completion
                print("  ✓ Test macro completed")
                print("  🎮 Your virtual controller is working correctly!")
                print("  📋 Games should now detect controller input from macros")
            else:
                print("  ✗ Failed to start test macro")
        else:
            print(f"\n⚠️  Virtual controller not working: {status.get('message', 'Unknown error')}")
            if platform.system() == "Windows":
                print("  💡 Make sure you have installed vgamepad: pip install vgamepad")
            elif platform.system() == "Linux":
                print("  💡 Linux virtual controller requires special permissions")
                print("     Try running with sudo or adding your user to the input group")
            else:
                print("  💡 Virtual controller not supported on this platform")
                print("     Macros will use keyboard/mouse simulation instead")
        
        print("\n" + "=" * 60)
        print("Test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        if platform.system() == "Windows":
            print("  pip install vgamepad")
        return False
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_virtual_controller()
    sys.exit(0 if success else 1)