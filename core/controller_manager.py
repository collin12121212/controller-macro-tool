"""
Controller management for detecting and reading controller inputs
"""

import pygame
import threading
import time

class ControllerManager:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        self.controllers = {}
        self.controller_states = {}
        self.monitoring = True
        
        self.start_monitoring()
        
    def start_monitoring(self):
        """Start monitoring for controller connections"""
        def monitor():
            while self.monitoring:
                try:
                    # Check for new controllers
                    pygame.event.pump()
                    
                    controller_count = pygame.joystick.get_count()
                    
                    # Initialize new controllers
                    for i in range(controller_count):
                        if i not in self.controllers:
                            try:
                                controller = pygame.joystick.Joystick(i)
                                controller.init()
                                self.controllers[i] = controller
                                print(f"Controller {i} connected: {controller.get_name()}")
                            except:
                                pass
                    
                    # Update controller states
                    self.update_controller_states()
                    
                    time.sleep(1/60)  # 60 FPS
                except:
                    pass
                    
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def update_controller_states(self):
        """Update the state of all connected controllers"""
        pygame.event.pump()
        
        for controller_id, controller in self.controllers.items():
            if controller.get_init():
                state = self.get_controller_input_state(controller)
                self.controller_states[controller_id] = state
                
    def get_controller_input_state(self, controller):
        """Get current input state from a controller"""
        state = {
            'buttons': {},
            'dpad': {},
            'sticks': {},
            'triggers': {}
        }
        
        try:
            # Get button states
            button_count = controller.get_numbuttons()
            button_names = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'Back', 'Start', 'LS', 'RS']
            
            for i in range(min(button_count, len(button_names))):
                state['buttons'][button_names[i]] = controller.get_button(i)
                
            # Get D-pad (hat) states
            if controller.get_numhats() > 0:
                hat = controller.get_hat(0)
                state['dpad']['left'] = hat[0] == -1
                state['dpad']['right'] = hat[0] == 1
                state['dpad']['up'] = hat[1] == 1
                state['dpad']['down'] = hat[1] == -1
                
            # Get analog stick states
            if controller.get_numaxes() >= 4:
                # Left stick
                left_x = controller.get_axis(0)
                left_y = controller.get_axis(1)
                state['sticks']['left'] = (left_x, left_y)
                
                # Right stick
                right_x = controller.get_axis(2)
                right_y = controller.get_axis(3)
                state['sticks']['right'] = (right_x, right_y)
                
            # Get trigger states
            if controller.get_numaxes() >= 6:
                # Triggers are typically on axes 4 and 5
                left_trigger = (controller.get_axis(4) + 1) / 2  # Convert from -1,1 to 0,1
                right_trigger = (controller.get_axis(5) + 1) / 2
                state['triggers']['LT'] = left_trigger
                state['triggers']['RT'] = right_trigger
                
        except Exception as e:
            print(f"Error reading controller state: {e}")
            
        return state
        
    def get_connected_controllers(self):
        """Get list of connected controllers"""
        return list(self.controllers.keys())
        
    def get_controller_state(self, controller_id):
        """Get current state of specific controller"""
        return self.controller_states.get(controller_id, None)
        
    def get_controller_name(self, controller_id):
        """Get name of specific controller"""
        if controller_id in self.controllers:
            return self.controllers[controller_id].get_name()
        return None
        
    def cleanup(self):
        """Cleanup resources"""
        self.monitoring = False
        
        for controller in self.controllers.values():
            if controller.get_init():
                controller.quit()
                
        pygame.joystick.quit()
        pygame.quit()