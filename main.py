#!/usr/bin/env python3
"""
Controller Macro Tool - Main Application
A comprehensive tool for recording and playing back controller macros with a modern GUI.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for required dependencies
try:
    import pygame
    import pynput
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError as e:
    print(f"Missing tkinter: {e}")
    print("Please install tkinter:")
    print("  Ubuntu/Debian: sudo apt-get install python3-tk")
    print("  CentOS/RHEL: sudo yum install tkinter")
    print("  macOS: tkinter should be included with Python")
    sys.exit(1)

import threading

from gui.main_window import MainWindow
from core.controller_manager import ControllerManager
from core.config_manager import ConfigManager

class ControllerMacroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.config_manager = ConfigManager()
        self.controller_manager = ControllerManager()
        self.main_window = None
        
        self.setup_application()
        
    def setup_application(self):
        """Initialize the application"""
        self.root.title("Controller Macro Tool")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap("assets/icons/app_icon.ico")
        except:
            pass
            
        # Apply dark theme
        self.apply_theme()
        
        # Initialize main window
        self.main_window = MainWindow(self.root, self.controller_manager, self.config_manager)
        
        # Setup shutdown handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def apply_theme(self):
        """Apply dark theme to the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TButton', background='#404040', foreground='white')
        style.configure('TEntry', background='#404040', foreground='white')
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#404040', foreground='white')
        
        self.root.configure(bg='#2b2b2b')
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
            
    def on_closing(self):
        """Handle application shutdown"""
        if self.main_window:
            self.main_window.cleanup()
        if self.controller_manager:
            self.controller_manager.cleanup()
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    app = ControllerMacroApp()
    app.run()