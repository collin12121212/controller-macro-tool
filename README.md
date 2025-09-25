# Controller Macro Tool

A comprehensive tool for recording and playing back controller macros with a modern GUI interface.

## Features

- 🎮 **Controller Support**: Works with various game controllers via pygame
- 📹 **Macro Recording**: Record complex controller input sequences
- ⚡ **Macro Playback**: Play back recorded macros with precision timing
- 🖥️ **Modern GUI**: Clean, dark-themed interface built with tkinter
- 💾 **Save/Load**: Save macros to JSON files for reuse
- ⚙️ **Configuration**: Customizable settings and key mappings
- 🔧 **Macro Editor**: Edit recorded macros with a visual timeline

## Installation

### Prerequisites

- Python 3.7 or higher
- A game controller connected to your system

### Platform-Specific Setup

#### Windows
1. Python should include tkinter by default
2. Connect your controller and ensure it's recognized by Windows

#### macOS
1. Python should include tkinter by default
2. You may need to install pygame dependencies:
   ```bash
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
   ```

#### Linux (Ubuntu/Debian)
1. Install tkinter and development packages:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-tk python3-dev
   ```

#### Linux (CentOS/RHEL/Fedora)
1. Install tkinter:
   ```bash
   sudo yum install tkinter
   # or on newer versions:
   sudo dnf install python3-tkinter
   ```

### Install Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/collin12121212/controller-macro-tool.git
   cd controller-macro-tool
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Application

```bash
python main.py
```

## Usage

### Getting Started

1. **Connect Controller**: Connect your game controller to your computer
2. **Launch Application**: Run `python main.py`
3. **Check Status**: Verify your controller is detected in the status bar
4. **Start Recording**: Click "Start Recording" and perform controller inputs
5. **Stop Recording**: Click "Stop Recording" when finished
6. **Name Your Macro**: Enter a descriptive name for your macro
7. **Save**: Your macro will be saved and appear in the Macro Library

### Recording Macros

1. Enter a name for your macro in the "Macro Name" field
2. Click "Start Recording" (button will turn red)
3. Perform the controller inputs you want to record
4. Click "Stop Recording" when finished
5. The macro will be automatically saved

### Playing Macros

1. Select a macro from the Macro Library list
2. Click "Play Selected Macro" or double-click the macro name
3. The macro will play back with the original timing

### Editing Macros

1. Select a macro from the library
2. The macro will appear in the Macro Editor panel
3. You can view the timeline of events
4. Use the editor controls to modify timing and events

### Saving and Loading

- **Auto-save**: Macros are automatically saved when recorded
- **Manual Save**: Use File → Save Macros to export to a specific location
- **Load**: Use File → Load Macros to import previously saved macros

## Troubleshooting

### Common Issues

#### "No module named 'tkinter'"
- **Linux**: Install python3-tk package
- **Windows/macOS**: Reinstall Python with tkinter support

#### "No module named 'pygame'"
```bash
pip install pygame>=2.6.0
```

#### "No module named 'pynput'"
```bash
pip install pynput>=1.7.6
```

#### Controller Not Detected
1. Ensure your controller is properly connected
2. Try disconnecting and reconnecting the controller
3. Check if the controller works in other applications
4. On Linux, you may need to run with sudo or add yourself to the input group:
   ```bash
   sudo usermod -a -G input $USER
   ```
   Then log out and log back in.

#### Application Won't Start
1. Check that all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Verify Python version is 3.7 or higher:
   ```bash
   python --version
   ```

#### Permission Issues (Linux)
If you get permission errors accessing the controller:
```bash
sudo chmod 666 /dev/input/event*
# Or add yourself to the input group (recommended):
sudo usermod -a -G input $USER
```

### Error Messages

#### "Missing dependency: No module named 'pygame'"
Run: `pip install pygame>=2.6.0`

#### "Missing dependency: No module named 'pynput'"
Run: `pip install pynput>=1.7.6`

#### "Missing tkinter"
Install tkinter for your platform (see installation instructions above)

## Configuration

The application creates a `config` directory with settings that can be customized:

- **Theme**: Dark theme (default)
- **Auto-save**: Automatically save macros (default: enabled)
- **Recording Quality**: High precision timing (default)
- **Key Mappings**: Customize controller button mappings
- **Window Geometry**: Remember window size and position

## File Structure

```
controller-macro-tool/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── core/                  # Core functionality
│   ├── config_manager.py  # Configuration and settings
│   ├── controller_manager.py # Controller input handling
│   ├── macro_recorder.py  # Macro recording logic
│   └── macro_player.py    # Macro playback logic
└── gui/                   # User interface
    ├── main_window.py     # Main application window
    ├── controller_display.py # Controller visualization
    └── macro_editor.py    # Macro editing interface
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your controller is working with other applications
4. Create an issue on the GitHub repository with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce the problem