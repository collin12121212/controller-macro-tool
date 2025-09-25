"""
Macro playback functionality
"""

import time
import threading
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

class MacroPlayer:
    def __init__(self, controller_manager):
        self.controller_manager = controller_manager
        self.playing = False
        self.playback_thread = None
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        
        # Virtual controller state for display updates during playback
        self.virtual_controller_state = {
            'buttons': {},
            'dpad': {},
            'sticks': {'left': (0.0, 0.0), 'right': (0.0, 0.0)},
            'triggers': {'LT': 0.0, 'RT': 0.0}
        }
        
        # Key mappings for controller buttons to keyboard keys
        self.key_mappings = {
            'A': Key.space,
            'B': 'x',
            'X': 'z',
            'Y': 'c',
            'LB': 'q',
            'RB': 'e',
            'Start': Key.enter,
            'Back': Key.esc,
            'dpad_up': Key.up,
            'dpad_down': Key.down,
            'dpad_left': Key.left,
            'dpad_right': Key.right,
            'LT': Key.shift_l,
            'RT': Key.ctrl_l
        }
        
    def play_macro(self, macro_events, settings=None):
        """Play a recorded macro"""
        # Use is_playing() method for consistent state checking
        if self.is_playing():
            return False
            
        if not macro_events:
            return False
            
        # Default settings
        if settings is None:
            settings = {'loops': 1, 'speed': 1.0}
            
        # Reset virtual state at start of playback
        self._reset_virtual_state()
            
        self.playing = True
        self.playback_thread = threading.Thread(
            target=self._playback_loop,
            args=(macro_events, settings),
            daemon=True
        )
        self.playback_thread.start()
        
        return True
        
    def stop_playback(self):
        """Stop current macro playback"""
        self.playing = False
        
        if self.playback_thread:
            self.playback_thread.join(timeout=2)
            # Ensure the thread reference is cleared after joining
            if not self.playback_thread.is_alive():
                self.playback_thread = None
        
        # Always reset virtual state when stopping
        self._reset_virtual_state()
            
    def _playback_loop(self, macro_events, settings):
        """Main playback loop"""
        try:
            loops = settings.get('loops', 1)
            speed_multiplier = settings.get('speed', 1.0)
            
            for loop_count in range(loops):
                if not self.playing:
                    break
                    
                # Reset timing for each loop
                start_time = time.time()
                last_timestamp = 0
                
                for event in macro_events:
                    if not self.playing:
                        break
                        
                    # Calculate delay
                    event_timestamp = event.get('timestamp', 0)
                    delay = (event_timestamp - last_timestamp) / speed_multiplier
                    
                    if delay > 0:
                        time.sleep(delay)
                        
                    # Execute event
                    self._execute_event(event)
                    last_timestamp = event_timestamp
                    
        except Exception as e:
            print(f"Error in playback loop: {e}")
        finally:
            self.playing = False
            self.playback_thread = None  # Clear thread reference when loop ends
            self._reset_virtual_state()  # Reset virtual state when playback ends
            
    def _execute_event(self, event):
        """Execute a single macro event"""
        try:
            event_type = event.get('type')
            button = event.get('button')
            value = event.get('value')
            
            # Update virtual controller state for display
            self._update_virtual_state(event_type, button, value)
            
            if event_type == 'button':
                self._execute_button_event(button, value)
            elif event_type == 'dpad':
                self._execute_button_event(button, value)
            elif event_type == 'trigger':
                self._execute_trigger_event(button, value)
            elif event_type == 'stick':
                self._execute_stick_event(button, value)
            elif event_type == 'delay':
                # Additional delay
                time.sleep(value / 1000.0)  # Convert ms to seconds
                
        except Exception as e:
            print(f"Error executing event: {e}")
            
    def _update_virtual_state(self, event_type, button, value):
        """Update virtual controller state for display purposes"""
        try:
            if event_type == 'button':
                self.virtual_controller_state['buttons'][button] = value
            elif event_type == 'dpad':
                self.virtual_controller_state['dpad'][button] = value
            elif event_type == 'trigger':
                self.virtual_controller_state['triggers'][button] = value
            elif event_type == 'stick':
                self.virtual_controller_state['sticks'][button] = value
        except Exception as e:
            print(f"Error updating virtual state: {e}")
            
    def _execute_button_event(self, button, pressed):
        """Execute a button press/release event"""
        key = self.key_mappings.get(button)
        if key is None:
            return
            
        try:
            if pressed:
                self.keyboard.press(key)
            else:
                self.keyboard.release(key)
        except Exception as e:
            print(f"Error executing button event {button}: {key} - {e}")
            
    def _execute_trigger_event(self, trigger, value):
        """Execute a trigger event"""
        # Map triggers to keys with pressure sensitivity simulation
        key = self.key_mappings.get(trigger)
        if key and value > 0.5:  # Threshold for activation
            try:
                self.keyboard.press(key)
                time.sleep(0.05)  # Brief hold
                self.keyboard.release(key)
            except Exception as e:
                print(f"Error executing trigger event {trigger}: {e}")
                
    def _execute_stick_event(self, stick, value):
        """Execute an analog stick event"""
        # Convert stick movement to mouse movement for demonstration
        try:
            if stick == 'stick_right':  # Use right stick for mouse
                x, y = value
                # Scale movement
                mouse_x = int(x * 50)  # Adjust sensitivity
                mouse_y = int(y * 50)
                
                if abs(mouse_x) > 5 or abs(mouse_y) > 5:  # Deadzone
                    current_pos = self.mouse.position
                    new_x = current_pos[0] + mouse_x
                    new_y = current_pos[1] + mouse_y
                    self.mouse.position = (new_x, new_y)
        except Exception as e:
            print(f"Error executing stick event {stick}: {e}")
            
    def is_playing(self):
        """Check if macro is currently playing"""
        # If playing flag is false, we're definitely not playing
        if not self.playing:
            return False
        
        # If there's no thread, we're not playing
        if not self.playback_thread:
            self.playing = False
            return False
            
        # If playing flag is true but thread is dead, reset the playing flag
        if not self.playback_thread.is_alive():
            self.playing = False  
            self.playback_thread = None
            return False
            
        return True
        
    def get_playback_status(self):
        """Get current playback status"""
        return {
            'playing': self.playing,
            'thread_alive': self.playback_thread.is_alive() if self.playback_thread else False
        }
        
    def get_virtual_controller_state(self):
        """Get the current virtual controller state during playback"""
        if self.is_playing():
            return self.virtual_controller_state.copy()
        return None
        
    def _reset_virtual_state(self):
        """Reset virtual controller state to default"""
        self.virtual_controller_state = {
            'buttons': {},
            'dpad': {},
            'sticks': {'left': (0.0, 0.0), 'right': (0.0, 0.0)},
            'triggers': {'LT': 0.0, 'RT': 0.0}
        }