"""
Real-time controller input visualization
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math

class ControllerDisplay:
    def __init__(self, parent, controller_manager):
        self.parent = parent
        self.controller_manager = controller_manager
        self.canvas_width = 300
        self.canvas_height = 400
        
        self.setup_display()
        self.start_update_thread()
        
    def setup_display(self):
        """Setup the controller display canvas"""
        display_frame = ttk.LabelFrame(self.parent, text="Controller Input", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(display_frame, width=self.canvas_width, height=self.canvas_height,
                               bg='#1e1e1e', highlightthickness=0)
        self.canvas.pack()
        
        self.draw_controller_template()
        
    def draw_controller_template(self):
        """Draw the controller template"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw controller body
        body_x1, body_y1 = 50, 100
        body_x2, body_y2 = 250, 300
        self.canvas.create_rectangle(body_x1, body_y1, body_x2, body_y2, 
                                   outline='white', width=2, fill='#333333')
        
        # Draw D-pad
        dpad_x, dpad_y = 90, 180
        dpad_size = 30
        self.draw_dpad(dpad_x, dpad_y, dpad_size)
        
        # Draw face buttons (A, B, X, Y)
        button_positions = {
            'A': (210, 200),
            'B': (230, 180),
            'X': (190, 180),
            'Y': (210, 160)
        }
        
        for button, (x, y) in button_positions.items():
            self.draw_button(button, x, y, 15, False)
            
        # Draw analog sticks
        self.draw_analog_stick('left', 90, 240, 20)
        self.draw_analog_stick('right', 210, 240, 20)
        
        # Draw triggers
        self.draw_trigger('LT', 70, 120, 30, 0)
        self.draw_trigger('RT', 200, 120, 30, 0)
        
        # Draw shoulder buttons
        self.draw_button('LB', 70, 140, 12, False)
        self.draw_button('RB', 200, 140, 12, False)
        
    def draw_dpad(self, x, y, size):
        """Draw D-pad"""
        # Up
        self.canvas.create_rectangle(x-5, y-size, x+5, y-5, outline='white', 
                                   tags='dpad_up', fill='#555555')
        # Down
        self.canvas.create_rectangle(x-5, y+5, x+5, y+size, outline='white', 
                                   tags='dpad_down', fill='#555555')
        # Left
        self.canvas.create_rectangle(x-size, y-5, x-5, y+5, outline='white', 
                                   tags='dpad_left', fill='#555555')
        # Right
        self.canvas.create_rectangle(x+5, y-5, x+size, y+5, outline='white', 
                                   tags='dpad_right', fill='#555555')
                                   
    def draw_button(self, name, x, y, radius, pressed):
        """Draw a circular button"""
        color = '#00ff00' if pressed else '#555555'
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                              outline='white', fill=color, tags=f'button_{name.lower()}')
        self.canvas.create_text(x, y, text=name, fill='white', font=('Arial', 8, 'bold'))
        
    def draw_analog_stick(self, name, center_x, center_y, radius):
        """Draw analog stick"""
        # Stick base
        self.canvas.create_oval(center_x-radius, center_y-radius, 
                              center_x+radius, center_y+radius,
                              outline='white', fill='#333333', tags=f'stick_{name}_base')
        
        # Stick position indicator
        self.canvas.create_oval(center_x-5, center_y-5, center_x+5, center_y+5,
                              outline='white', fill='#0078d4', tags=f'stick_{name}_pos')
                              
    def draw_trigger(self, name, x, y, width, value):
        """Draw trigger with pressure visualization"""
        height = 10
        fill_height = int(height * value)
        
        # Trigger background
        self.canvas.create_rectangle(x, y, x+width, y+height, outline='white', 
                                   fill='#555555', tags=f'trigger_{name.lower()}_bg')
        
        # Trigger fill (pressure indicator)
        if fill_height > 0:
            self.canvas.create_rectangle(x, y+height-fill_height, x+width, y+height,
                                       fill='#00ff00', tags=f'trigger_{name.lower()}_fill')
        
        # Label
        self.canvas.create_text(x+width//2, y-5, text=name, fill='white', 
                              font=('Arial', 8, 'bold'))
                              
    def update_display(self, controller_state):
        """Update display with current controller state"""
        if not controller_state:
            return
            
        # Update buttons
        buttons = controller_state.get('buttons', {})
        for button_name, pressed in buttons.items():
            if button_name.lower() in ['a', 'b', 'x', 'y', 'lb', 'rb']:
                color = '#00ff00' if pressed else '#555555'
                try:
                    self.canvas.itemconfig(f'button_{button_name.lower()}', fill=color)
                except:
                    pass
                    
        # Update D-pad
        dpad = controller_state.get('dpad', {})
        for direction, pressed in dpad.items():
            color = '#00ff00' if pressed else '#555555'
            try:
                self.canvas.itemconfig(f'dpad_{direction}', fill=color)
            except:
                pass
                
        # Update analog sticks
        sticks = controller_state.get('sticks', {})
        for stick_name, (x_val, y_val) in sticks.items():
            try:
                # Calculate stick position
                if stick_name == 'left':
                    center_x, center_y = 90, 240
                else:
                    center_x, center_y = 210, 240
                    
                # Convert stick values (-1 to 1) to pixel positions
                pixel_x = center_x + int(x_val * 15)  # 15 pixel range
                pixel_y = center_y + int(y_val * 15)
                
                # Update stick position
                coords = self.canvas.coords(f'stick_{stick_name}_pos')
                if coords:
                    self.canvas.coords(f'stick_{stick_name}_pos', 
                                     pixel_x-5, pixel_y-5, pixel_x+5, pixel_y+5)
            except:
                pass
                
        # Update triggers
        triggers = controller_state.get('triggers', {})
        for trigger_name, value in triggers.items():
            try:
                # Remove old fill
                self.canvas.delete(f'trigger_{trigger_name.lower()}_fill')
                
                # Draw new fill based on value
                if trigger_name.lower() == 'lt':
                    x, y = 70, 120
                else:
                    x, y = 200, 120
                    
                width, height = 30, 10
                fill_height = int(height * value)
                
                if fill_height > 0:
                    self.canvas.create_rectangle(x, y+height-fill_height, x+width, y+height,
                                               fill='#00ff00', tags=f'trigger_{trigger_name.lower()}_fill')
            except:
                pass
                
    def start_update_thread(self):
        """Start the display update thread"""
        def update_loop():
            while True:
                try:
                    controllers = self.controller_manager.get_connected_controllers()
                    if controllers:
                        # Get state of first controller
                        controller_state = self.controller_manager.get_controller_state(0)
                        if controller_state:
                            # Schedule UI update on main thread
                            self.parent.after(0, lambda: self.update_display(controller_state))
                    time.sleep(1/60)  # 60 FPS update rate
                except:
                    break
                    
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()