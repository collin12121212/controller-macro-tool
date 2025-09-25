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
    def __init__(self, root, controller_manager, config_manager):
        self.root = root
        self.controller_manager = controller_manager
        self.config_manager = config_manager
        self.macro_recorder = MacroRecorder(controller_manager)
        self.macro_player = MacroPlayer(controller_manager)
        
        self.is_recording = False
        self.current_macro = None
        self.macros = {}
        
        self.setup_ui()
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
        
    def setup_left_panel(self):
        """Setup left panel with controller display"""
        left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(left_frame, weight=1)
        
        # Controller display
        controller_label = ttk.Label(left_frame, text="Controller Status", font=('Arial', 12, 'bold'))
        controller_label.pack(pady=(0, 10))
        
        self.controller_display = ControllerDisplay(left_frame, self.controller_manager)
        
        # Recording controls
        controls_frame = ttk.LabelFrame(left_frame, text="Recording Controls", padding=10)
        controls_frame.pack(fill=tk.X, pady=10)
        
        self.record_button = ttk.Button(controls_frame, text="Start Recording", 
                                       command=self.toggle_recording, width=15)
        self.record_button.pack(pady=5)
        
        self.stop_button = ttk.Button(controls_frame, text="Stop All", 
                                     command=self.stop_all, state=tk.DISABLED, width=15)
        self.stop_button.pack(pady=5)
        
        # Macro name entry
        name_frame = ttk.Frame(controls_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Macro Name:").pack(anchor=tk.W)
        self.macro_name_var = tk.StringVar(value="New Macro")
        self.macro_name_entry = ttk.Entry(name_frame, textvariable=self.macro_name_var)
        self.macro_name_entry.pack(fill=tk.X, pady=(2, 0))
        
        # Recording status
        self.recording_status = ttk.Label(controls_frame, text="Ready to record", 
                                        foreground='green')
        self.recording_status.pack(pady=5)
        
    def setup_center_panel(self):
        """Setup center panel with macro list"""
        center_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(center_frame, weight=1)
        
        # Macro list
        list_label = ttk.Label(center_frame, text="Macro Library", font=('Arial', 12, 'bold'))
        list_label.pack(pady=(0, 10))
        
        # Macro listbox with scrollbar
        list_frame = ttk.Frame(center_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.macro_listbox = tk.Listbox(list_frame, bg='#404040', fg='white', 
                                       selectbackground='#0078d4')
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.macro_listbox.yview)
        self.macro_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.macro_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.macro_listbox.bind('<<ListboxSelect>>', self.on_macro_select)
        self.macro_listbox.bind('<Double-1>', self.play_selected_macro)
        
        # Macro management buttons
        button_frame = ttk.Frame(center_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Play", command=self.play_selected_macro).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Edit", command=self.edit_selected_macro).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Delete", command=self.delete_selected_macro).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Save", command=self.save_macros).pack(side=tk.RIGHT, padx=2)
        ttk.Button(button_frame, text="Load", command=self.load_macros).pack(side=tk.RIGHT, padx=2)
        
    def setup_right_panel(self):
        """Setup right panel with macro editor"""
        right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(right_frame, weight=2)
        
        # Macro editor
        editor_label = ttk.Label(right_frame, text="Macro Editor", font=('Arial', 12, 'bold'))
        editor_label.pack(pady=(0, 10))
        
        self.macro_editor = MacroEditor(right_frame, self.config_manager)
        
    def setup_status_bar(self):
        """Setup bottom status bar"""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Controller status
        self.controller_status_label = ttk.Label(self.status_frame, text="No controller detected")
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
                macro_name = self.macro_name_var.get().strip()
                if not macro_name:
                    macro_name = f"Macro_{len(self.macros) + 1}"
                    
                self.macros[macro_name] = macro_data
                self.update_macro_list()
                self.status_label.configure(text=f"Recorded macro '{macro_name}' with {len(macro_data)} inputs")
            else:
                self.status_label.configure(text="No inputs recorded")
                
        self.record_button.configure(text="Start Recording")
        self.stop_button.configure(state=tk.DISABLED)
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