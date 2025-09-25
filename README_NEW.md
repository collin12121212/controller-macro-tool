# Controller Macro Tool

A comprehensive, modern tool for recording and playing back controller macros with a professional GUI interface.

## ✨ Features

### 🎮 **Controller Support**
- Works with various game controllers via pygame
- Real-time controller input visualization with modern Xbox-style layout
- Realistic button animations and pressure-sensitive trigger displays
- Support for D-pad, analog sticks, face buttons, and shoulder buttons

### 📹 **Advanced Macro Recording**
- High-precision macro recording with 120Hz sampling rate
- Automatic input optimization and duplicate event removal
- Support for complex controller input sequences
- Smart macro naming with automatic unique ID generation

### ⚡ **Intelligent Macro Playback**
- Precise timing reproduction with configurable speed multipliers
- Loop support with customizable repeat counts
- Error handling and playback status monitoring
- Thread-safe execution with proper resource management

### 🎨 **Modern GUI Interface**
- Professional dark theme with blue/purple gradient accents
- Glassmorphism effects and smooth animations
- Card-based layout with proper visual hierarchy
- Modern typography and spacing
- Real-time status updates and progress indicators

### 🔥 **Global Hotkey System**
- Background hotkey monitoring (works when app is minimized)
- Customizable keyboard shortcuts:
  - **Ctrl+R**: Start/Stop Recording
  - **Ctrl+P**: Play Last Macro
  - **Ctrl+S**: Stop All Operations
  - **F9**: Quick Record Toggle
  - **F10**: Emergency Stop
- Support for F1-F12 and Ctrl+key combinations

### 📚 **Advanced Macro Management**
- Comprehensive macro library with metadata tracking
- Search and filter functionality by name, description, or tags
- Favorites system for quick access to frequently used macros
- Usage statistics and analytics
- Macro chaining for complex automation sequences
- Import/export with full metadata preservation

### 🔔 **Smart Notification System**
- Toast-style notifications with different types (info, success, warning, error)
- Status bar with color-coded messages
- Context-aware user guidance and feedback
- Non-intrusive notification positioning

### 💾 **Data Management**
- Auto-save functionality with backup options
- JSON-based storage format for portability
- Batch import/export capabilities
- Recent files tracking and quick access

### 🛡️ **Security & Reliability**
- Comprehensive error handling throughout the application
- Input validation and sanitization
- Memory management for large macro libraries
- Thread-safe operations and proper resource cleanup

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

### Platform-Specific Setup

#### Windows
```bash
# Python should include tkinter by default
pip install -r requirements.txt
```

#### macOS
```bash
# tkinter should be included with Python
pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev
pip install -r requirements.txt
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install tkinter python3-devel
pip install -r requirements.txt
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python3 main.py
```

## 📖 Usage

### Getting Started
1. **Launch the application** - Run `python3 main.py`
2. **Connect your controller** - The app will automatically detect connected controllers
3. **Start recording** - Click "Start Recording" or press **Ctrl+R**
4. **Use your controller** - Perform the inputs you want to record
5. **Stop recording** - Click "Stop Recording" or press **Ctrl+R** again
6. **Play back** - Select your macro from the library and click "Play" or press **Ctrl+P**

### Global Hotkeys
The application supports global hotkeys that work even when minimized:

| Hotkey | Action |
|--------|--------|
| **Ctrl+R** | Start/Stop Recording |
| **Ctrl+P** | Play Last Macro |
| **Ctrl+S** | Stop All Operations |
| **F9** | Quick Record Toggle |
| **F10** | Emergency Stop |

## 🧪 Testing

Run the comprehensive test suite:
```bash
python3 test_functionality.py
```

## 📁 File Structure

```
controller-macro-tool/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── test_functionality.py     # Comprehensive test suite
├── README.md                 # This documentation
├── core/                     # Core functionality
│   ├── config_manager.py     # Configuration and settings
│   ├── controller_manager.py # Controller input handling
│   ├── macro_recorder.py     # Macro recording logic
│   ├── macro_player.py       # Macro playback logic
│   ├── macro_manager.py      # Advanced macro management
│   └── hotkey_manager.py     # Global hotkey system
└── gui/                      # User interface
    ├── main_window.py        # Main application window
    ├── controller_display.py # Controller visualization
    ├── macro_editor.py       # Macro editing interface
    ├── theme_manager.py      # Modern theme system
    └── notification_manager.py # Toast notifications
```

## 🏆 What's New in Version 2.0

### Major Enhancements
- ✅ **Complete UI Overhaul**: Modern dark theme with professional styling
- ✅ **Global Hotkey System**: Background hotkey support with customizable shortcuts
- ✅ **Enhanced Controller Display**: Realistic Xbox-style layout with animations
- ✅ **Advanced Macro Management**: Search, favorites, statistics, and chaining
- ✅ **Smart Notifications**: Toast-style notifications with context-aware feedback
- ✅ **Improved Error Handling**: Comprehensive validation and user guidance
- ✅ **Performance Optimizations**: Faster rendering and reduced memory usage
- ✅ **Security Enhancements**: Input validation and secure file operations

### Bug Fixes
- ✅ Fixed macro playbook execution errors with pynput key handling
- ✅ Resolved macro naming/storage issues with unique counter system
- ✅ Enhanced controller input detection and processing
- ✅ Improved memory management and resource cleanup

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Run the test suite to identify problems
3. Create a GitHub issue with detailed information

---

**Created with ❤️ for the gaming and automation community**