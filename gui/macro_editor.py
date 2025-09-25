"""
Macro editor interface for editing recorded macros
"""

import tkinter as tk
from tkinter import ttk
import time

class MacroEditor:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.current_macro = None
        self.edit_mode = False
        
        self.setup_editor()
        
    def setup_editor(self):
        """Setup the macro editor interface"""
        editor_frame = ttk.LabelFrame(self.parent, text="Macro Timeline", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar_frame = ttk.Frame(editor_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.edit_button = ttk.Button(toolbar_frame, text="Edit Mode", 
                                     command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar_frame, text="Add Delay", 
                  command=self.add_delay).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar_frame, text="Remove Selected", 
                  command=self.remove_selected).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar_frame, text="Clear All", 
                  command=self.clear_macro).pack(side=tk.RIGHT, padx=2)
        
        # Macro settings
        settings_frame = ttk.LabelFrame(editor_frame, text="Settings", padding=5)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Loop settings
        loop_frame = ttk.Frame(settings_frame)
        loop_frame.pack(fill=tk.X)
        
        ttk.Label(loop_frame, text="Loops:").pack(side=tk.LEFT)
        self.loop_var = tk.StringVar(value="1")
        loop_spinbox = ttk.Spinbox(loop_frame, from_=1, to=999, width=5, 
                                  textvariable=self.loop_var)
        loop_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Speed multiplier
        speed_frame = ttk.Frame(settings_frame)
        speed_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=3.0, 
                               orient=tk.HORIZONTAL, variable=self.speed_var)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.RIGHT)
        
        speed_scale.configure(command=self.on_speed_change)
        
        # Timeline view
        timeline_frame = ttk.Frame(editor_frame)
        timeline_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for macro events
        columns = ('Time', 'Type', 'Button', 'Value', 'Duration')
        self.timeline_tree = ttk.Treeview(timeline_frame, columns=columns, show='headings')
        
        for col in columns:
            self.timeline_tree.heading(col, text=col)
            self.timeline_tree.column(col, width=80)
            
        # Scrollbar for treeview
        timeline_scrollbar = ttk.Scrollbar(timeline_frame, orient=tk.VERTICAL, 
                                          command=self.timeline_tree.yview)
        self.timeline_tree.configure(yscrollcommand=timeline_scrollbar.set)
        
        self.timeline_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        timeline_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.timeline_tree.bind('<Double-1>', self.edit_event)
        
    def load_macro(self, macro_data):
        """Load macro data into the editor"""
        self.current_macro = macro_data.copy() if macro_data else []
        self.update_timeline_view()
        
    def update_timeline_view(self):
        """Update the timeline view with current macro data"""
        # Clear existing items
        for item in self.timeline_tree.get_children():
            self.timeline_tree.delete(item)
            
        if not self.current_macro:
            return
            
        # Add macro events to timeline
        for i, event in enumerate(self.current_macro):
            timestamp = event.get('timestamp', 0)
            event_type = event.get('type', 'unknown')
            button = event.get('button', '')
            value = event.get('value', '')
            duration = event.get('duration', 0)
            
            # Format timestamp
            time_str = f"{timestamp:.3f}s"
            
            # Format value based on type
            if event_type == 'button':
                value_str = "Pressed" if value else "Released"
            elif event_type == 'axis':
                value_str = f"{value:.2f}"
            elif event_type == 'delay':
                value_str = f"{value}ms"
            else:
                value_str = str(value)
                
            duration_str = f"{duration}ms" if duration > 0 else ""
            
            self.timeline_tree.insert('', 'end', values=(
                time_str, event_type, button, value_str, duration_str
            ))
            
    def set_edit_mode(self, enabled):
        """Enable or disable edit mode"""
        self.edit_mode = enabled
        if enabled:
            self.edit_button.configure(text="View Mode")
        else:
            self.edit_button.configure(text="Edit Mode")
            
    def toggle_edit_mode(self):
        """Toggle edit mode"""
        self.set_edit_mode(not self.edit_mode)
        
    def add_delay(self):
        """Add a custom delay to the macro"""
        if not self.edit_mode:
            return
            
        # Create delay input dialog
        delay_window = tk.Toplevel(self.parent)
        delay_window.title("Add Delay")
        delay_window.geometry("300x150")
        delay_window.transient(self.parent)
        delay_window.grab_set()
        
        # Center the window
        delay_window.update_idletasks()
        x = (delay_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (delay_window.winfo_screenheight() // 2) - (150 // 2)
        delay_window.geometry(f"300x150+{x}+{y}")
        
        # Delay input
        ttk.Label(delay_window, text="Delay (milliseconds):").pack(pady=10)
        delay_var = tk.StringVar(value="100")
        delay_entry = ttk.Entry(delay_window, textvariable=delay_var, width=10)
        delay_entry.pack(pady=5)
        delay_entry.focus()
        delay_entry.select_range(0, tk.END)
        
        # Buttons
        button_frame = ttk.Frame(delay_window)
        button_frame.pack(pady=20)
        
        def add_delay_action():
            try:
                delay_ms = float(delay_var.get())
                if delay_ms > 0:
                    # Add delay event to current macro
                    delay_event = {
                        'type': 'delay',
                        'timestamp': 0,  # Will be recalculated
                        'button': 'delay',
                        'value': delay_ms,
                        'duration': 0
                    }
                    
                    # Insert at selected position or end
                    selection = self.timeline_tree.selection()
                    if selection:
                        index = self.timeline_tree.index(selection[0])
                        self.current_macro.insert(index + 1, delay_event)
                    else:
                        self.current_macro.append(delay_event)
                        
                    self.update_timeline_view()
                    delay_window.destroy()
            except ValueError:
                pass
                
        ttk.Button(button_frame, text="Add", command=add_delay_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=delay_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        delay_entry.bind('<Return>', lambda e: add_delay_action())
        
    def remove_selected(self):
        """Remove selected events from macro"""
        if not self.edit_mode or not self.current_macro:
            return
            
        selection = self.timeline_tree.selection()
        if selection:
            # Get indices of selected items
            indices = [self.timeline_tree.index(item) for item in selection]
            indices.sort(reverse=True)  # Remove from end to start
            
            # Remove events
            for index in indices:
                if 0 <= index < len(self.current_macro):
                    del self.current_macro[index]
                    
            self.update_timeline_view()
            
    def clear_macro(self):
        """Clear all events from macro"""
        if not self.edit_mode:
            return
            
        if tk.messagebox.askyesno("Clear Macro", "Remove all events from macro?"):
            self.current_macro = []
            self.update_timeline_view()
            
    def edit_event(self, event):
        """Edit selected event"""
        if not self.edit_mode:
            return
            
        selection = self.timeline_tree.selection()
        if not selection or not self.current_macro:
            return
            
        item_index = self.timeline_tree.index(selection[0])
        if 0 <= item_index < len(self.current_macro):
            event_data = self.current_macro[item_index]
            # Open edit dialog for the event
            self.open_event_edit_dialog(event_data, item_index)
            
    def open_event_edit_dialog(self, event_data, index):
        """Open dialog to edit event properties"""
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Edit Event")
        edit_window.geometry("400x300")
        edit_window.transient(self.parent)
        edit_window.grab_set()
        
        # Center the window
        edit_window.update_idletasks()
        x = (edit_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (edit_window.winfo_screenheight() // 2) - (300 // 2)
        edit_window.geometry(f"400x300+{x}+{y}")
        
        # Event properties
        main_frame = ttk.Frame(edit_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Type
        ttk.Label(main_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value=event_data.get('type', ''))
        ttk.Label(main_frame, text=type_var.get()).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Button
        ttk.Label(main_frame, text="Button:").grid(row=1, column=0, sticky=tk.W, pady=5)
        button_var = tk.StringVar(value=event_data.get('button', ''))
        ttk.Label(main_frame, text=button_var.get()).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Value (editable for delays)
        ttk.Label(main_frame, text="Value:").grid(row=2, column=0, sticky=tk.W, pady=5)
        value_var = tk.StringVar(value=str(event_data.get('value', '')))
        if event_data.get('type') == 'delay':
            value_entry = ttk.Entry(main_frame, textvariable=value_var)
            value_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        else:
            ttk.Label(main_frame, text=value_var.get()).grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Duration
        ttk.Label(main_frame, text="Duration:").grid(row=3, column=0, sticky=tk.W, pady=5)
        duration_var = tk.StringVar(value=str(event_data.get('duration', 0)))
        duration_entry = ttk.Entry(main_frame, textvariable=duration_var)
        duration_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_changes():
            try:
                # Update event data
                if event_data.get('type') == 'delay':
                    event_data['value'] = float(value_var.get())
                event_data['duration'] = float(duration_var.get())
                
                # Update the macro
                self.current_macro[index] = event_data
                self.update_timeline_view()
                edit_window.destroy()
            except ValueError:
                pass
                
        ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def on_speed_change(self, value):
        """Handle speed scale change"""
        speed_value = float(value)
        self.speed_label.configure(text=f"{speed_value:.1f}x")
        
    def get_macro_settings(self):
        """Get current macro settings"""
        return {
            'loops': int(self.loop_var.get()),
            'speed': float(self.speed_var.get())
        }
        
    def get_edited_macro(self):
        """Get the edited macro data"""
        return self.current_macro