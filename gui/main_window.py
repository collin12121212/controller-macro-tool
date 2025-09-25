"""
Main GUI Window for Controller Macro Tool
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

from .controller_display import ControllerDisplay
from .macro_editor import MacroEditor
from core.macro_recorder import MacroRecorder
from core.macro_player import MacroPlayer

class MainWindow:
    def __init__(self, root, controller_manager, config_manager, theme_manager, hotkey_manager):
        self.root = root
        self.controller_manager = controller_manager
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.hotkey_manager = hotkey_manager
        self.macro_recorder = MacroRecorder(controller_manager)
        self.macro_player = MacroPlayer(controller_manager)
        
        self.is_recording = False
        self.current_macro = None
        self.macros = {}
        self.macro_counter = 1  # Fix for macro naming issue
        
        self.setup_ui()
        self.setup_hotkeys()
        self.start_controller_monitoring()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window for resizable panels
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controller display and controls
        self.setup_left_panel()
        
        # Center panel - Macro list
        self.setup_center_panel()
        
        # Right panel - Macro editor
        self.setup_right_panel()
        
        # Bottom status bar
        self.setup_status_bar()
        
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        # Register hotkey callbacks
        self.hotkey_manager.register_callback('start_stop_recording', self.toggle_recording)
        self.hotkey_manager.register_callback('play_last_macro', self.play_last_macro)
        self.hotkey_manager.register_callback('stop_all', self.stop_all)
        self.hotkey_manager.register_callback('quick_record', self.quick_record)
        self.hotkey_manager.register_callback('emergency_stop', self.emergency_stop)
        
        # Start monitoring
        self.hotkey_manager.start_monitoring()
        
    def setup_left_panel(self):
        """Setup left panel with controller display"""
        left_frame = self.theme_manager.create_card_frame(self.paned_window)
        self.paned_window.add(left_frame, weight=1)
        
        # Header
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        controller_label = ttk.Label(header_frame, text="Controller Status", style='Heading.TLabel')
        controller_label.pack(anchor=tk.W)
        
        # Controller display
        self.controller_display = ControllerDisplay(left_frame, self.controller_manager)
        
        # Recording controls card
        controls_frame = self.theme_manager.create_card_frame(left_frame)
        controls_frame.pack(fill=tk.X, padx=20, pady=20)
        
        controls_header = ttk.Label(controls_frame, text="Recording Controls", style='Heading.TLabel')
        controls_header.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Button container
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.record_button = self.theme_manager.create_gradient_button(
            button_frame, "Start Recording", self.toggle_recording, 'Primary'
        )
        self.record_button.pack(fill=tk.X, pady=5)
        
        self.stop_button = self.theme_manager.create_gradient_button(
            button_frame, "Stop All", self.stop_all, 'Danger'
        )
        self.stop_button.pack(fill=tk.X, pady=5)
        self.stop_button.configure(state=tk.DISABLED)
        
        # Macro name entry
        name_frame = ttk.Frame(controls_frame)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(name_frame, text="Macro Name:", style='TLabel').pack(anchor=tk.W)
        self.macro_name_var = tk.StringVar(value="")
        self.macro_name_entry = ttk.Entry(name_frame, textvariable=self.macro_name_var)
        self.macro_name_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Recording status
        self.recording_status = ttk.Label(controls_frame, text="Ready to record", 
                                        style='TLabel', foreground=self.theme_manager.get_color('success'))
        self.recording_status.pack(padx=20, pady=(0, 20))
        
    def setup_center_panel(self):
        """Setup center panel with macro list"""
        center_frame = self.theme_manager.create_card_frame(self.paned_window)
        self.paned_window.add(center_frame, weight=1)
        
        # Header
        header_frame = ttk.Frame(center_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        list_label = ttk.Label(header_frame, text="Macro Library", style='Heading.TLabel')
        list_label.pack(anchor=tk.W)
        
        # Macro listbox with scrollbar
        list_frame = ttk.Frame(center_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create custom listbox with modern styling
        self.macro_listbox = tk.Listbox(
            list_frame, 
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('text_primary'),
            selectbackground=self.theme_manager.get_color('accent_blue'),
            selectforeground=self.theme_manager.get_color('text_primary'),
            borderwidth=0,
            highlightthickness=0,
            font=self.theme_manager.get_font('default')
        )
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.macro_listbox.yview)
        self.macro_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.macro_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.macro_listbox.bind('<<ListboxSelect>>', self.on_macro_select)
        self.macro_listbox.bind('<Double-Button-1>', self.play_selected_macro)
        
        # Macro control buttons
        button_frame = ttk.Frame(center_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Create modern buttons in a grid
        btn_style_frame = ttk.Frame(button_frame)
        btn_style_frame.pack(fill=tk.X)
        
        play_btn = self.theme_manager.create_gradient_button(
            btn_style_frame, "▶ Play", self.play_selected_macro, 'Success'
        )
        play_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        edit_btn = self.theme_manager.create_gradient_button(
            btn_style_frame, "✏ Edit", self.edit_selected_macro, 'Primary'
        )
        edit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        delete_btn = self.theme_manager.create_gradient_button(
            btn_style_frame, "🗑 Delete", self.delete_selected_macro, 'Danger'
        )
        delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # File operations
        file_frame = ttk.Frame(button_frame)
        file_frame.pack(fill=tk.X, pady=(10, 0))
        
        save_btn = ttk.Button(file_frame, text="💾 Save Library", command=self.save_macros)
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        load_btn = ttk.Button(file_frame, text="📁 Load Library", command=self.load_macros)
        load_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def setup_right_panel(self):
        """Setup right panel with macro editor"""
        right_frame = self.theme_manager.create_card_frame(self.paned_window)
        self.paned_window.add(right_frame, weight=2)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        editor_label = ttk.Label(header_frame, text="Macro Editor", style='Heading.TLabel')
        editor_label.pack(anchor=tk.W)
        
        # Hotkey info card
        hotkey_card = self.theme_manager.create_card_frame(right_frame)
        hotkey_card.pack(fill=tk.X, padx=20, pady=10)
        
        hotkey_header = ttk.Label(hotkey_card, text="Global Hotkeys", style='TLabel')
        hotkey_header.pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        hotkeys_info = [
            "Ctrl+R: Start/Stop Recording",
            "Ctrl+P: Play Last Macro", 
            "Ctrl+S: Stop All",
            "F9: Quick Record",
            "F10: Emergency Stop"
        ]
        
        for hotkey in hotkeys_info:
            hotkey_label = ttk.Label(hotkey_card, text=f"• {hotkey}", style='Muted.TLabel')
            hotkey_label.pack(anchor=tk.W, padx=25, pady=2)
        
        # Add some padding at bottom
        ttk.Label(hotkey_card, text="").pack(pady=5)
        
        # Macro editor
        self.macro_editor = MacroEditor(right_frame, self.config_manager)
        
    def setup_status_bar(self):
        """Setup bottom status bar"""
        self.status_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status content
        status_content = ttk.Frame(self.status_frame)
        status_content.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(status_content, text="Ready", style='TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Controller status with modern styling
        self.controller_status_label = ttk.Label(
            status_content, 
            text="🎮 No controller detected", 
            style='Muted.TLabel'
        )
        self.controller_status_label.pack(side=tk.RIGHT)
        
    def start_controller_monitoring(self):
        """Start monitoring controller status"""
        def monitor():
            while True:
                try:
                    controllers = self.controller_manager.get_connected_controllers()
                    if controllers:
                        status_text = f"{len(controllers)} controller(s) connected"
                        self.controller_status_label.configure(foreground='green')
                    else:
                        status_text = "No controller detected"
                        self.controller_status_label.configure(foreground='red')
                    
                    self.root.after(0, lambda: self.controller_status_label.configure(text=status_text))
                    time.sleep(1)
                except:
                    break
                    
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def toggle_recording(self):
        """Toggle macro recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording a new macro"""
        if not self.controller_manager.get_connected_controllers():
            messagebox.showerror("Error", "No controller detected!")
            return
            
        self.is_recording = True
        self.record_button.configure(text="Stop Recording", style='Accent.TButton')
        self.stop_button.configure(state=tk.NORMAL)
        self.recording_status.configure(text="Recording...", foreground='red')
        
        # Start recording in separate thread
        def record():
            self.current_macro = self.macro_recorder.start_recording()
            
        thread = threading.Thread(target=record, daemon=True)
        thread.start()
        
    def stop_recording(self):
        """Stop recording and save macro"""
        if self.is_recording:
            self.is_recording = False
            macro_data = self.macro_recorder.stop_recording()
            
            if macro_data and len(macro_data) > 0:
                # Get macro name from input or generate unique name
                macro_name = getattr(self, 'macro_name_var', None)
                if macro_name:
                    macro_name = macro_name.get().strip()
                
                if not macro_name:
                    # Generate unique name
                    base_name = f"Macro_{self.macro_counter}"
                    while base_name in self.macros:
                        self.macro_counter += 1
                        base_name = f"Macro_{self.macro_counter}"
                    macro_name = base_name
                    self.macro_counter += 1
                    
                self.macros[macro_name] = macro_data
                self.update_macro_list()
                self.status_label.configure(text=f"Recorded macro '{macro_name}' with {len(macro_data)} inputs")
            else:
                self.status_label.configure(text="No inputs recorded")
                
        # Update UI elements if they exist
        if hasattr(self, 'record_button'):
            self.record_button.configure(text="Start Recording")
        if hasattr(self, 'stop_button'):
            self.stop_button.configure(state=tk.DISABLED)
        if hasattr(self, 'recording_status'):
            self.recording_status.configure(text="Ready to record", foreground='green')
        
    def stop_all(self):
        """Stop all recording and playback"""
        self.stop_recording()
        self.macro_player.stop_playback()
        self.status_label.configure(text="All operations stopped")
        
    def on_macro_select(self, event):
        """Handle macro selection"""
        selection = self.macro_listbox.curselection()
        if selection:
            macro_name = self.macro_listbox.get(selection[0])
            if macro_name in self.macros:
                self.macro_editor.load_macro(self.macros[macro_name])
                
    def play_selected_macro(self, event=None):
        """Play the selected macro"""
        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a macro to play")
            return
            
        macro_name = self.macro_listbox.get(selection[0])
        if macro_name in self.macros:
            def play():
                self.status_label.configure(text=f"Playing macro '{macro_name}'...")
                self.macro_player.play_macro(self.macros[macro_name])
                self.root.after(0, lambda: self.status_label.configure(text="Playback completed"))
                
            thread = threading.Thread(target=play, daemon=True)
            thread.start()
            
    def edit_selected_macro(self):
        """Edit the selected macro"""
        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a macro to edit")
            return
            
        macro_name = self.macro_listbox.get(selection[0])
        if macro_name in self.macros:
            self.macro_editor.load_macro(self.macros[macro_name])
            self.macro_editor.set_edit_mode(True)
            
    def delete_selected_macro(self):
        """Delete the selected macro"""
        selection = self.macro_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a macro to delete")
            return
            
        macro_name = self.macro_listbox.get(selection[0])
        if messagebox.askyesno("Confirm Delete", f"Delete macro '{macro_name}'?"):
            del self.macros[macro_name]
            self.update_macro_list()
            self.status_label.configure(text=f"Deleted macro '{macro_name}'")
            
    def update_macro_list(self):
        """Update the macro listbox"""
        self.macro_listbox.delete(0, tk.END)
        for macro_name in sorted(self.macros.keys()):
            self.macro_listbox.insert(tk.END, macro_name)
            
    def save_macros(self):
        """Save macros to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.config_manager.save_macros(self.macros, file_path)
                self.status_label.configure(text=f"Macros saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save macros: {str(e)}")
                
    def load_macros(self):
        """Load macros from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                loaded_macros = self.config_manager.load_macros(file_path)
                self.macros.update(loaded_macros)
                self.update_macro_list()
                self.status_label.configure(text=f"Loaded {len(loaded_macros)} macros from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load macros: {str(e)}")
                
    def cleanup(self):
        """Cleanup resources"""
        if self.is_recording:
            self.stop_recording()
        self.macro_player.stop_playback()
        
    # Hotkey callback methods
    def play_last_macro(self):
        """Play the most recently created or used macro"""
        if not self.macros:
            return
            
        # Get the last macro (by creation order or most recent)
        last_macro_name = list(self.macros.keys())[-1]
        macro_data = self.macros[last_macro_name]
        
        if macro_data:
            self.macro_player.play_macro(macro_data)
            self.status_label.configure(text=f"Playing macro '{last_macro_name}' via hotkey")
            
    def quick_record(self):
        """Quick record with auto-generated name"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def emergency_stop(self):
        """Emergency stop all operations"""
        self.stop_all()
        self.status_label.configure(text="Emergency stop activated!", foreground=self.theme_manager.get_color('error'))