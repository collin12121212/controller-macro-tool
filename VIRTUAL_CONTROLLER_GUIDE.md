# Virtual Controller Guide - Controller Macro Tool

## Overview
This guide explains the virtual controller functionality that ensures your game macros are properly recognized by games.

## The Problem
Many games don't recognize keyboard/mouse simulation as controller input. When you recorded a controller macro but played it back using keyboard simulation, games would ignore the input.

## The Solution
The tool now creates a virtual Xbox 360 controller that games recognize as a real controller. Your macros are played through this virtual controller, ensuring perfect game compatibility.

## Platform Support

### Windows (Full Support)
- ✅ Virtual Xbox 360 controller via `vgamepad`
- ✅ Full DirectInput/XInput compatibility
- ✅ All buttons, triggers, and analog sticks supported
- ✅ Games detect real controller input

**Installation:**
```bash
pip install vgamepad
```

### Linux (Limited Support)
- ⚠️ Virtual controller requires special permissions
- 🔄 Falls back to keyboard/mouse simulation
- 💡 Future support planned with `uinput`

**Troubleshooting:**
```bash
# Add user to input group
sudo usermod -a -G input $USER
# Or run with sudo (not recommended)
sudo python main.py
```

### macOS (Fallback Only)
- 🔄 Uses keyboard/mouse simulation
- 📝 Virtual controller support not available

## How to Test Virtual Controller

Run the test script to check your system:
```bash
python test_virtual_controller.py
```

Expected output on Windows:
```
✓ Virtual Xbox 360 controller initialized and tested successfully
  Games should now detect controller input during macro playback
Playback Method: Virtual Controller (Xbox 360)
```

## Status Messages Explained

### Success Messages
- `✓ Virtual Xbox 360 controller initialized and tested successfully` - Everything working perfectly
- `✓ Keyboard/mouse controllers initialized successfully` - Fallback system ready

### Warning Messages
- `⚠️ Permission denied for virtual controller` - Need to run with elevated permissions (Linux)
- `⚠️ Virtual controller library not available` - Need to install vgamepad (Windows)

### Error Messages
- `✗ Failed to initialize virtual controller` - Hardware or system issue
- `✗ Error with virtual controller button X` - Runtime error, falling back to keyboard

## Troubleshooting

### Game Still Not Detecting Input
1. **Check the status**: Run `test_virtual_controller.py`
2. **Verify platform**: Windows has best support
3. **Check permissions**: Linux requires special setup
4. **Restart the application**: Try closing and reopening
5. **Check game settings**: Some games need controller input enabled

### Virtual Controller Not Working
1. **Windows**: Install vgamepad with `pip install vgamepad`
2. **Linux**: Run with sudo or configure permissions
3. **Check logs**: Look for error messages in console output
4. **Fallback mode**: The tool will use keyboard/mouse if virtual controller fails

### Performance Issues
1. **Close other controller software**: Xbox Accessories, Steam Input, etc.
2. **Check CPU usage**: Virtual controller has minimal overhead
3. **Reduce macro complexity**: Very rapid inputs might cause issues

## Technical Details

### Virtual Controller Features
- **Xbox 360 compatibility**: Uses standard XInput protocol
- **All inputs supported**: Buttons, D-pad, triggers, analog sticks
- **Automatic fallback**: Switches to keyboard/mouse if virtual controller fails
- **Error recovery**: Handles disconnections and permission issues gracefully

### Input Mapping
- Buttons: A, B, X, Y, LB, RB, Start, Back, LS, RS
- D-pad: Up, Down, Left, Right
- Triggers: LT, RT (with analog values)
- Sticks: Left stick, Right stick (with analog values)

### Safety Features
- **Permission checks**: Detects and reports permission issues
- **Graceful degradation**: Falls back to keyboard/mouse simulation
- **Error logging**: Detailed error messages for troubleshooting
- **Status monitoring**: Real-time status checking

## FAQ

**Q: Will this work with all games?**
A: On Windows with virtual controller: Yes, works with any game that supports Xbox controllers. With keyboard/mouse fallback: Depends on the game.

**Q: Do I need a real controller connected?**
A: No, the virtual controller works independently of any physical controllers.

**Q: Can I use both virtual controller and real controller?**
A: Yes, they work together without conflicts.

**Q: Why does Linux support require permissions?**
A: Linux virtual input devices require special permissions for security reasons.

**Q: Is this safe for anti-cheat systems?**
A: The virtual controller appears as a standard Xbox controller to games and anti-cheat systems.