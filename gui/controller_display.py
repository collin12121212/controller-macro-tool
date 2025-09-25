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
    def __init__(self, parent, controller_manager, macro_player=None):
        self.parent = parent
        self.controller_manager = controller_manager
        self.macro_player = macro_player  # Add macro_player for virtual state access
        self.canvas_width = 300  # Will be updated in setup_display
        self.canvas_height = 240
        
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
        self.stick_positions = {'left': (0.0, 0.0), 'right': (0.0, 0.0)}
        self.trigger_values = {'LT': 0.0, 'RT': 0.0}
        
        self.setup_display()
        self.start_update_thread()
        
    def setup_display(self):
        """Setup the modern controller display canvas"""
        # Create container frame with reduced padding for more compact layout
        display_container = ttk.Frame(self.parent)
        display_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Title with smaller font
        title_label = ttk.Label(display_container, text="Controller Input", style='TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Canvas with modern styling - reduced size for compact layout
        self.canvas_width = 300
        self.canvas_height = 240
        
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
        # Scaled points for smaller canvas (300x240)
        body_points = [
            # Top curve
            70, 75,   # Top left start
            110, 70,  # Top left curve
            150, 70,  # Top center left
            150, 70,  # Top center
            190, 70,  # Top center right
            230, 75,  # Top right curve
            250, 80,  # Top right
            
            # Right side
            260, 90,  # Right shoulder start
            265, 110, # Right shoulder end
            265, 140, # Right side
            260, 160, # Right grip start
            245, 180, # Right grip curve
            220, 200, # Right grip middle
            190, 215, # Right grip bottom
            
            # Bottom center
            160, 220, # Right center bottom
            150, 222, # Center right
            150, 222, # Center
            140, 220, # Center left
            110, 215, # Left center bottom
            
            # Left side
            80, 200,  # Left grip bottom
            55, 180,  # Left grip curve
            40, 160,  # Left grip start
            35, 140,  # Left side
            35, 110,  # Left shoulder end
            40, 90,   # Left shoulder start
            50, 80,   # Left top
        ]
        
        self.canvas.create_polygon(
            body_points,
            fill=self.colors['controller_body'],
            outline=self.colors['controller_outline'],
            width=2,
            smooth=True,
            tags="controller_body"
        )
        
        # Add subtle inner highlight for depth
        inner_points = [
            80, 85,   # Top left
            150, 80,  # Top center
            220, 85,  # Top right
            250, 100, # Right shoulder
            250, 150, # Right side
            210, 190, # Right grip
            160, 205, # Right bottom
            140, 205, # Center bottom
            90, 190,  # Left grip
            50, 150,  # Left side
            50, 100,  # Left shoulder
        ]
        
        self.canvas.create_polygon(
            inner_points,
            fill='',
            outline='#404040',
            width=1,
            smooth=True,
            tags="controller_highlight"
        )
        
    def draw_modern_dpad(self):
        """Draw modern D-pad with individual directional buttons"""
        center_x, center_y = 85, 130
        button_size = 10
        
        # D-pad directions
        directions = {
            'up': (center_x, center_y - 18),
            'down': (center_x, center_y + 18),
            'left': (center_x - 18, center_y),
            'right': (center_x + 18, center_y)
        }
        
        # Draw D-pad base
        self.canvas.create_oval(
            center_x - 22, center_y - 22,
            center_x + 22, center_y + 22,
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
                    x - 5, y - button_size,
                    x + 5, y + button_size,
                    fill=color,
                    outline=self.colors['controller_outline'],
                    width=1,
                    tags=f"dpad_{direction}"
                )
            else:
                # Horizontal rectangles
                self.canvas.create_rectangle(
                    x - button_size, y - 5,
                    x + button_size, y + 5,
                    fill=color,
                    outline=self.colors['controller_outline'],
                    width=1,
                    tags=f"dpad_{direction}"
                )
                
    def draw_face_buttons(self):
        """Draw modern face buttons (A, B, X, Y) with labels and glow effects"""
        center_x, center_y = 215, 130
        button_radius = 13
        
        # Button positions (Xbox layout)
        buttons = {
            'A': (center_x, center_y + 18, '#00b56a'),      # Green
            'B': (center_x + 18, center_y, '#e74856'),       # Red  
            'X': (center_x - 18, center_y, '#0078d4'),       # Blue
            'Y': (center_x, center_y - 18, '#ff8c00')        # Orange
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
                font=('Arial', 10, 'bold'),
                tags=f"button_{button}_text"
            )
            
    def draw_analog_sticks(self):
        """Draw analog sticks with movement indication"""
        # Left stick
        left_x, left_y = 85, 180
        # Right stick  
        right_x, right_y = 215, 180
        
        for stick_name, (base_x, base_y) in [('left', (left_x, left_y)), ('right', (right_x, right_y))]:
            # Get stick position from controller state
            stick_pos = self.get_stick_position(stick_name)
            
            # Base/housing
            self.canvas.create_oval(
                base_x - 18, base_y - 18,
                base_x + 18, base_y + 18,
                fill=self.colors['stick_normal'],
                outline=self.colors['controller_outline'],
                width=2,
                tags=f"stick_{stick_name}_base"
            )
            
            # Movement indicator (small circle that moves)
            offset_x = stick_pos[0] * 13  # Scale for smaller canvas
            offset_y = -stick_pos[1] * 13  # Invert Y axis for correct direction
            
            # Clamp to base circle
            distance = math.sqrt(offset_x**2 + offset_y**2)
            if distance > 13:
                offset_x = (offset_x / distance) * 13
                offset_y = (offset_y / distance) * 13
            
            stick_x = base_x + offset_x
            stick_y = base_y + offset_y
            
            # Stick cap with improved visual feedback
            pressed = distance > 0.05  # Lower threshold for more responsive feedback
            cap_color = self.colors['stick_pressed'] if pressed else self.colors['button_normal']
            
            self.canvas.create_oval(
                stick_x - 7, stick_y - 7,
                stick_x + 7, stick_y + 7,
                fill=cap_color,
                outline=self.colors['controller_outline'],
                width=1,
                tags=f"stick_{stick_name}_cap"
            )
            
            # Add deadzone visualization
            if distance > 0.05:
                self.canvas.create_oval(
                    base_x - 2, base_y - 2,
                    base_x + 2, base_y + 2,
                    fill=self.colors['accent'],
                    outline='',
                    tags=f"stick_{stick_name}_center"
                )
            
    def draw_shoulder_buttons(self):
        """Draw shoulder buttons (LB/RB)"""
        # Left shoulder
        lb_pressed = self.button_states.get('LB', False)
        lb_color = self.colors['button_pressed'] if lb_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            40, 60, 75, 75,
            fill=lb_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="shoulder_lb"
        )
        self.canvas.create_text(57, 67, text="LB", fill=self.colors['button_text'], 
                              font=('Arial', 7, 'bold'), tags="shoulder_lb_text")
        
        # Right shoulder
        rb_pressed = self.button_states.get('RB', False)
        rb_color = self.colors['button_pressed'] if rb_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            225, 60, 260, 75,
            fill=rb_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="shoulder_rb"
        )
        self.canvas.create_text(242, 67, text="RB", fill=self.colors['button_text'],
                              font=('Arial', 7, 'bold'), tags="shoulder_rb_text")
        
    def draw_triggers(self):
        """Draw trigger pressure bars (LT/RT)"""
        # Left trigger
        lt_value = self.get_trigger_value('LT')
        lt_fill_height = int(18 * lt_value)
        
        # Trigger background
        self.canvas.create_rectangle(
            32, 40, 45, 58,
            fill=self.colors['trigger_bg'],
            outline=self.colors['controller_outline'],
            width=1,
            tags="trigger_lt_bg"
        )
        
        # Trigger fill
        if lt_fill_height > 0:
            self.canvas.create_rectangle(
                33, 58 - lt_fill_height, 44, 57,
                fill=self.colors['trigger_fill'],
                outline='',
                tags="trigger_lt_fill"
            )
        
        self.canvas.create_text(38, 32, text="LT", fill=self.colors['button_text'],
                              font=('Arial', 7, 'bold'), tags="trigger_lt_text")
        
        # Right trigger
        rt_value = self.get_trigger_value('RT')
        rt_fill_height = int(18 * rt_value)
        
        # Trigger background
        self.canvas.create_rectangle(
            255, 40, 268, 58,
            fill=self.colors['trigger_bg'],
            outline=self.colors['controller_outline'],
            width=1,
            tags="trigger_rt_bg"
        )
        
        # Trigger fill
        if rt_fill_height > 0:
            self.canvas.create_rectangle(
                256, 58 - rt_fill_height, 267, 57,
                fill=self.colors['trigger_fill'],
                outline='',
                tags="trigger_rt_fill"
            )
        
        self.canvas.create_text(261, 32, text="RT", fill=self.colors['button_text'],
                              font=('Arial', 7, 'bold'), tags="trigger_rt_text")
        
    def draw_center_buttons(self):
        """Draw center buttons (Start, Back/Select)"""
        # Back/Select button
        back_pressed = self.button_states.get('Back', False)
        back_color = self.colors['button_pressed'] if back_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            125, 95, 138, 108,
            fill=back_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="center_back"
        )
        self.canvas.create_text(131, 101, text="◀◀", fill=self.colors['button_text'],
                              font=('Arial', 6), tags="center_back_text")
        
        # Start button
        start_pressed = self.button_states.get('Start', False)
        start_color = self.colors['button_pressed'] if start_pressed else self.colors['button_normal']
        
        self.canvas.create_rectangle(
            162, 95, 175, 108,
            fill=start_color,
            outline=self.colors['controller_outline'],
            width=1,
            tags="center_start"
        )
        self.canvas.create_text(168, 101, text="▶▶", fill=self.colors['button_text'],
                              font=('Arial', 6), tags="center_start_text")
        
    def get_stick_position(self, stick_name):
        """Get normalized stick position (-1 to 1)"""
        return self.stick_positions.get(stick_name, (0.0, 0.0))
        
    def get_trigger_value(self, trigger_name):
        """Get trigger pressure value (0 to 1)"""
        return self.trigger_values.get(trigger_name, 0.0)
        
    def update_display(self, controller_state):
        """Update display with current controller state"""
        if not controller_state:
            return
            
        # Update button states
        buttons = controller_state.get('buttons', {})
        dpad = controller_state.get('dpad', {})
        triggers = controller_state.get('triggers', {})
        sticks = controller_state.get('sticks', {})
        
        # Merge all button states
        self.button_states.update(buttons)
        for direction, pressed in dpad.items():
            self.button_states[f'dpad_{direction}'] = pressed
        self.button_states.update(triggers)
        
        # Update stick positions
        self.stick_positions.update(sticks)
        
        # Update trigger values
        self.trigger_values.update(triggers)
        
        # Redraw controller with updated states
        self.draw_modern_controller()
        
    def start_update_thread(self):
        """Start the display update thread"""
        def update_loop():
            while True:
                try:
                    # Check if macro is playing and get virtual state first
                    if self.macro_player and self.macro_player.is_playing():
                        virtual_state = self.macro_player.get_virtual_controller_state()
                        if virtual_state:
                            self.parent.after(0, lambda: self.update_display(virtual_state))
                        else:
                            # Fallback to real controller if virtual state unavailable
                            controllers = self.controller_manager.get_connected_controllers()
                            if controllers:
                                controller_id = controllers[0]
                                state = self.controller_manager.get_controller_state(controller_id)
                                if state:
                                    self.parent.after(0, lambda: self.update_display(state))
                    else:
                        # Normal operation - show real controller input
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
