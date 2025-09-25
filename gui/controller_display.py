"""
Modern Real-time Controller Input Visualization
Enhanced with realistic Xbox/PlayStation controller layouts and smooth animations
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
        self.canvas_width = 340
        self.canvas_height = 280
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'controller_body': '#2d2d30',
            'controller_outline': '#555555',
            'button_normal': '#3e3e42',
            'button_pressed': '#0078d4',
            'button_text': '#ffffff',
            'accent': '#0078d4',
            'accent_glow': '#106ebe',
            'dpad': '#2a2a2a',
            'stick_normal': '#333333',
            'stick_pressed': '#0078d4',
            'trigger_bg': '#2a2a2a',
            'trigger_fill': '#00b56a'
        }
        
        # Animation states
        self.button_states = {}
        self.animation_states = {}
        
        self.setup_display()
        self.start_update_thread()
        
    def setup_display(self):
        """Setup the modern controller display canvas"""
        # Create container frame
        display_container = ttk.Frame(self.parent)
        display_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title
        title_label = ttk.Label(display_container, text="Controller Input", style='TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Canvas with modern styling
        self.canvas = tk.Canvas(
            display_container, 
            width=self.canvas_width, 
            height=self.canvas_height,
            bg=self.colors['bg'], 
            highlightthickness=1,
            highlightcolor=self.colors['controller_outline'],
            relief='flat'
        )
        self.canvas.pack()
        
        self.draw_modern_controller()
        
    def draw_modern_controller(self):
        """Draw a modern, realistic controller layout"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Controller body with rounded appearance
        self.draw_controller_body()
        
        # Draw components
        self.draw_modern_dpad()
        self.draw_face_buttons()
        self.draw_analog_sticks()
        self.draw_shoulder_buttons()
        self.draw_triggers()
        self.draw_center_buttons()
        
    def draw_controller_body(self):
        """Draw the main controller body with modern styling"""
        # Main body outline (Xbox-style)
        body_points = [
            60, 80,   # Top left
            280, 80,  # Top right
            300, 100, # Right shoulder
            300, 180, # Right bottom
            200, 220, # Right grip bottom
            180, 240, # Right grip curve
            160, 240, # Right grip inner
            140, 220, # Center bottom right
            120, 220, # Center bottom left
            100, 240, # Left grip inner
            80, 240,  # Left grip curve
            60, 220,  # Left grip bottom
            40, 180,  # Left bottom
            40, 100,  # Left shoulder
        ]
        
        self.canvas.create_polygon(
            body_points,
            fill=self.colors['controller_body'],
            outline=self.colors['controller_outline'],
            width=2,
            smooth=True,
            tags="controller_body"
        )
        
        # Add subtle inner highlight
        inner_points = [
            70, 90,
            270, 90,
            290, 110,
            290, 170,
            190, 210,
            170, 225,
            150, 225,
            130, 210,
            110, 210,
            90, 225,
            70, 225,
            50, 210,
            50, 110,
        ]
        
        self.canvas.create_polygon(
            inner_points,
            fill='',
            outline='#444444',
            width=1,
            smooth=True,
            tags="controller_highlight"
        )
        
    def draw_modern_dpad(self):
        """Draw modern D-pad with individual directional buttons"""
        center_x, center_y = 100, 150
        button_size = 12
        
        # D-pad directions
        directions = {
            'up': (center_x, center_y - 20),
            'down': (center_x, center_y + 20),
            'left': (center_x - 20, center_y),
            'right': (center_x + 20, center_y)
        }
        
        # Draw D-pad base
        self.canvas.create_oval(
            center_x - 25, center_y - 25,
            center_x + 25, center_y + 25,
            fill=self.colors['dpad'],
            outline=self.colors['controller_outline'],
            width=1,
            tags="dpad_base"
        )
        
        # Draw directional buttons
        for direction, (x, y) in directions.items():
            pressed = self.button_states.get(f'dpad_{direction}', False)
            color = self.colors['button_pressed'] if pressed else self.colors['button_normal']
            
            # Create directional button
            if direction in ['up', 'down']:
                # Vertical rectangles
                self.canvas.create_rectangle(
                    x - 6, y - button_size,
                    x + 6, y + button_size,
                    fill=color,
                    outline=self.colors['controller_outline'],
                    width=1,
                    tags=f"dpad_{direction}"
                )
            else:
                # Horizontal rectangles
                self.canvas.create_rectangle(
                    x - button_size, y - 6,
                    x + button_size, y + 6,
                    fill=color,
                    outline=self.colors['controller_outline'],
                    width=1,
                    tags=f"dpad_{direction}"
                )
                
    def draw_face_buttons(self):
        """Draw modern face buttons (A, B, X, Y) with labels and glow effects"""
        center_x, center_y = 240, 150
        button_radius = 15
        
        # Button positions (Xbox layout)
        buttons = {
            'A': (center_x, center_y + 20, '#00b56a'),      # Green
            'B': (center_x + 20, center_y, '#e74856'),       # Red  
            'X': (center_x - 20, center_y, '#0078d4'),       # Blue
            'Y': (center_x, center_y - 20, '#ff8c00')        # Orange
        }
        
        for button, (x, y, default_color) in buttons.items():
            pressed = self.button_states.get(button, False)
            
            if pressed:
                # Glow effect when pressed
                for i in range(3, 0, -1):
                    alpha = 0.3 * i
                    self.canvas.create_oval(
                        x - button_radius - i*2, y - button_radius - i*2,
                        x + button_radius + i*2, y + button_radius + i*2,
                        fill=default_color,
                        outline='',
                        stipple='gray25',
                        tags=f"button_{button}_glow"
                    )
                
                color = default_color
            else:
                color = self.colors['button_normal']
            
            # Main button
            self.canvas.create_oval(
                x - button_radius, y - button_radius,
                x + button_radius, y + button_radius,
                fill=color,
                outline=self.colors['controller_outline'],
                width=2,
                tags=f"button_{button}"
            )
            
            # Button label
            self.canvas.create_text(
                x, y,
                text=button,
                fill=self.colors['button_text'],
                font=('Arial', 12, 'bold'),
                tags=f"button_{button}_text"
            )
            
    def draw_analog_sticks(self):
        """Draw analog sticks with movement indication"""
        # Left stick
        left_x, left_y = 100, 200
        # Right stick  
        right_x, right_y = 240, 200
        
        for stick_name, (base_x, base_y) in [('left', (left_x, left_y)), ('right', (right_x, right_y))]:
            # Get stick position (if available from controller state)
            stick_pos = self.get_stick_position(stick_name)
            
            # Base/housing
            self.canvas.create_oval(
                base_x - 20, base_y - 20,
                base_x + 20, base_y + 20,
                fill=self.colors['stick_normal'],
                outline=self.colors['controller_outline'],
                width=2,
                tags=f"stick_{stick_name}_base"
            )
            
            # Movement indicator (small circle that moves)
            offset_x = stick_pos[0] * 12  # Scale movement
            offset_y = stick_pos[1] * 12
            
            # Clamp to base circle
            distance = math.sqrt(offset_x**2 + offset_y**2)
            if distance > 12:
                offset_x = (offset_x / distance) * 12
                offset_y = (offset_y / distance) * 12
            
            stick_x = base_x + offset_x
            stick_y = base_y + offset_y
            
            # Stick cap
            pressed = distance > 0.1
            cap_color = self.colors['stick_pressed'] if pressed else self.colors['button_normal']
            
            self.canvas.create_oval(
                stick_x - 8, stick_y - 8,
                stick_x + 8, stick_y + 8,
                fill=cap_color,
                outline=self.colors['controller_outline'],
                width=1,
                tags=f"stick_{stick_name}_cap"
            )
            
    def draw_shoulder_buttons(self):
        """Draw shoulder buttons (LB/RB)"""
        # Left shoulder
        lb_pressed = self.button_states.get('LB', False)
        lb_color = self.colors['button_pressed'] if lb_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            50, 70, 90, 90,
            fill=lb_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="shoulder_lb"
        )
        self.canvas.create_text(70, 80, text="LB", fill=self.colors['button_text'], 
                              font=('Arial', 8, 'bold'), tags="shoulder_lb_text")
        
        # Right shoulder
        rb_pressed = self.button_states.get('RB', False)
        rb_color = self.colors['button_pressed'] if rb_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            250, 70, 290, 90,
            fill=rb_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="shoulder_rb"
        )
        self.canvas.create_text(270, 80, text="RB", fill=self.colors['button_text'],
                              font=('Arial', 8, 'bold'), tags="shoulder_rb_text")
        
    def draw_triggers(self):
        """Draw trigger pressure bars (LT/RT)"""
        # Left trigger
        lt_value = self.get_trigger_value('LT')
        lt_fill_height = int(20 * lt_value)
        
        # Trigger background
        self.canvas.create_rectangle(
            40, 50, 55, 70,
            fill=self.colors['trigger_bg'],
            outline=self.colors['controller_outline'],
            width=1,
            tags="trigger_lt_bg"
        )
        
        # Trigger fill
        if lt_fill_height > 0:
            self.canvas.create_rectangle(
                41, 70 - lt_fill_height, 54, 69,
                fill=self.colors['trigger_fill'],
                outline='',
                tags="trigger_lt_fill"
            )
        
        self.canvas.create_text(47, 40, text="LT", fill=self.colors['button_text'],
                              font=('Arial', 8, 'bold'), tags="trigger_lt_text")
        
        # Right trigger
        rt_value = self.get_trigger_value('RT')
        rt_fill_height = int(20 * rt_value)
        
        # Trigger background
        self.canvas.create_rectangle(
            285, 50, 300, 70,
            fill=self.colors['trigger_bg'],
            outline=self.colors['controller_outline'],
            width=1,
            tags="trigger_rt_bg"
        )
        
        # Trigger fill
        if rt_fill_height > 0:
            self.canvas.create_rectangle(
                286, 70 - rt_fill_height, 299, 69,
                fill=self.colors['trigger_fill'],
                outline='',
                tags="trigger_rt_fill"
            )
        
        self.canvas.create_text(292, 40, text="RT", fill=self.colors['button_text'],
                              font=('Arial', 8, 'bold'), tags="trigger_rt_text")
        
    def draw_center_buttons(self):
        """Draw center buttons (Start, Back/Select)"""
        # Back/Select button
        back_pressed = self.button_states.get('Back', False)
        back_color = self.colors['button_pressed'] if back_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            140, 110, 155, 125,
            fill=back_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="center_back"
        )
        self.canvas.create_text(147, 117, text="◀◀", fill=self.colors['button_text'],
                              font=('Arial', 8), tags="center_back_text")
        
        # Start button
        start_pressed = self.button_states.get('Start', False)
        start_color = self.colors['button_pressed'] if start_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            185, 110, 200, 125,
            fill=start_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="center_start"
        )
        self.canvas.create_text(192, 117, text="▶▶", fill=self.colors['button_text'],
                              font=('Arial', 8), tags="center_start_text")
        
    def get_stick_position(self, stick_name):
        """Get normalized stick position (-1 to 1)"""
        # This would get actual data from controller manager
        # For now, return default position
        return (0.0, 0.0)
        
    def get_trigger_value(self, trigger_name):
        """Get trigger pressure value (0 to 1)"""
        # This would get actual data from controller manager
        # For now, return default value
        return self.button_states.get(trigger_name, 0.0)
        
    def update_display(self, controller_state):
        """Update display with current controller state"""
        if not controller_state:
            return
            
        # Update button states
        buttons = controller_state.get('buttons', {})
        dpad = controller_state.get('dpad', {})
        triggers = controller_state.get('triggers', {})
        
        # Merge all button states
        self.button_states.update(buttons)
        for direction, pressed in dpad.items():
            self.button_states[f'dpad_{direction}'] = pressed
        self.button_states.update(triggers)
        
        # Redraw controller with updated states
        self.draw_modern_controller()
        
    def start_update_thread(self):
        """Start the display update thread"""
        def update_loop():
            while True:
                try:
                    controllers = self.controller_manager.get_connected_controllers()
                    if controllers:
                        controller_id = controllers[0]
                        state = self.controller_manager.get_controller_state(controller_id)
                        if state:
                            self.parent.after(0, lambda: self.update_display(state))
                    
                    time.sleep(1/30)  # 30 FPS update rate
                except Exception as e:
                    print(f"Controller display update error: {e}")
                    time.sleep(1)
                    
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
