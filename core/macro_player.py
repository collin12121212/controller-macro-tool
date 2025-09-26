"""
Macro playback functionality
"""

import time
import threading
import platform
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# Try to import virtual controller libraries based on platform
virtual_controller_available = False
try:
    system = platform.system()
    if system == "Windows":
        import vgamepad as vg
        virtual_controller_available = True
        virtual_controller_type = "vgamepad"
    elif system == "Linux":
        # For Linux, we could use uinput but it requires special permissions
        # For now, we'll use keyboard/mouse simulation
        virtual_controller_available = False
        virtual_controller_type = "none"
    else:
        virtual_controller_available = False
        virtual_controller_type = "none"
except ImportError:
    virtual_controller_available = False
    virtual_controller_type = "none"

class MacroPlayer:
    def __init__(self, controller_manager):
        self.controller_manager = controller_manager
        self.playing = False
        self.playback_thread = None
        
        # Initialize keyboard/mouse controllers with error handling
        self.keyboard = None
        self.mouse = None
        self._setup_input_controllers()
        
        # Virtual controller setup
        self.virtual_controller = None
        self.use_virtual_controller = False
        self._setup_virtual_controller()
        
        # Virtual controller state for display updates during playback
        self.virtual_controller_state = {
            'buttons': {},
            'dpad': {},
            'sticks': {'left': (0.0, 0.0), 'right': (0.0, 0.0)},
            'triggers': {'LT': 0.0, 'RT': 0.0}
        }
        
        # Key mappings for controller buttons to keyboard keys (fallback)
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
    
    def _setup_input_controllers(self):
        """Initialize keyboard and mouse controllers with error handling"""
        try:
            self.keyboard = KeyboardController()
            self.mouse = MouseController()
            print("✓ Keyboard/mouse controllers initialized successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize keyboard/mouse controllers: {e}")
            print("  Input simulation may not work in headless environments")
            self.keyboard = None
            self.mouse = None
        
    def _setup_virtual_controller(self):
        """Initialize virtual controller if available"""
        global virtual_controller_available, virtual_controller_type
        
        if virtual_controller_available and virtual_controller_type == "vgamepad":
            try:
                # Ensure vgamepad is available by checking the global import
                if 'vg' not in globals():
                    raise ImportError("vgamepad module not available")
                    
                self.virtual_controller = vg.VX360Gamepad()
                # Test the virtual controller with a quick button press/release
                self.virtual_controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.virtual_controller.update()
                self.virtual_controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.virtual_controller.update()
                
                self.use_virtual_controller = True
                print("✓ Virtual Xbox 360 controller initialized and tested successfully")
                print("  Games should now detect controller input during macro playback")
            except PermissionError as e:
                print(f"✗ Permission denied for virtual controller: {e}")
                print("  Linux users may need to run with sudo or add user to input group")
                print("  Falling back to keyboard/mouse simulation")
                self.virtual_controller = None
                self.use_virtual_controller = False
            except ImportError as e:
                print(f"✗ Virtual controller library not available: {e}")
                print("  Falling back to keyboard/mouse simulation")
                self.virtual_controller = None
                self.use_virtual_controller = False
            except Exception as e:
                print(f"✗ Failed to initialize virtual controller: {e}")
                print("  Falling back to keyboard/mouse simulation")
                self.virtual_controller = None
                self.use_virtual_controller = False
        else:
            print(f"Virtual controller not available on {platform.system()}. Using keyboard/mouse simulation.")
            self.use_virtual_controller = False
            
    def get_playback_method(self):
        """Get the current playback method being used"""
        if self.use_virtual_controller and self.virtual_controller:
            return "Virtual Controller (Xbox 360)"
        else:
            return "Keyboard/Mouse Simulation"
    
    def check_virtual_controller_status(self):
        """Check the current status of the virtual controller"""
        status = {
            'available': virtual_controller_available,
            'type': virtual_controller_type,
            'initialized': self.use_virtual_controller and self.virtual_controller is not None,
            'platform': platform.system()
        }
        
        if self.use_virtual_controller and self.virtual_controller:
            try:
                # Test virtual controller with a quick operation
                self.virtual_controller.update()
                status['working'] = True
                status['message'] = "Virtual controller is working correctly"
            except Exception as e:
                status['working'] = False
                status['message'] = f"Virtual controller error: {e}"
                # Disable if it's not working
                self.use_virtual_controller = False
                self.virtual_controller = None
        else:
            status['working'] = False
            if virtual_controller_available:
                status['message'] = "Virtual controller initialization failed"
            else:
                status['message'] = f"Virtual controller not supported on {platform.system()}"
        
        return status
        
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
                # Normalize stick names: 'stick_left' -> 'left', 'stick_right' -> 'right'
                if button.startswith('stick_'):
                    stick_name = button[6:]  # Remove 'stick_' prefix
                else:
                    stick_name = button
                self.virtual_controller_state['sticks'][stick_name] = value
        except Exception as e:
            print(f"Error updating virtual state: {e}")
            
    def _execute_button_event(self, button, pressed):
        """Execute a button press/release event"""
        if self.use_virtual_controller and self.virtual_controller:
            self._execute_virtual_button_event(button, pressed)
        else:
            self._execute_keyboard_button_event(button, pressed)
            
    def _execute_virtual_button_event(self, button, pressed):
        """Execute button event using virtual controller"""
        try:
            if virtual_controller_type == "vgamepad" and self.virtual_controller:
                # Map controller buttons to vgamepad buttons
                button_map = {
                    'A': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                    'B': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
                    'X': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
                    'Y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
                    'LB': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                    'RB': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                    'Start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
                    'Back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
                    'LS': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                    'RS': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                    'dpad_up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
                    'dpad_down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
                    'dpad_left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
                    'dpad_right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
                }
                
                vg_button = button_map.get(button)
                if vg_button:
                    if pressed:
                        self.virtual_controller.press_button(button=vg_button)
                    else:
                        self.virtual_controller.release_button(button=vg_button)
                    # Always call update() to ensure the input is sent to the system
                    self.virtual_controller.update()
                else:
                    print(f"⚠️  Unknown button '{button}' - not mapped for virtual controller")
                    
        except Exception as e:
            print(f"✗ Error with virtual controller button {button}: {e}")
            print("  Virtual controller may have been disconnected, falling back to keyboard")
            # Disable virtual controller on persistent errors
            self.use_virtual_controller = False
            self.virtual_controller = None
            # Fall back to keyboard simulation
            self._execute_keyboard_button_event(button, pressed)
            
    def _execute_keyboard_button_event(self, button, pressed):
        """Execute button event using keyboard simulation"""
        if not self.keyboard:
            print(f"⚠️  Keyboard controller not available - cannot simulate {button}")
            return
            
        key = self.key_mappings.get(button)
        if key is None:
            print(f"⚠️  Button '{button}' not mapped to keyboard key")
            return
            
        try:
            if pressed:
                self.keyboard.press(key)
            else:
                self.keyboard.release(key)
        except Exception as e:
            print(f"✗ Error executing keyboard button event {button}: {key} - {e}")
            print("  This may be due to missing X server or permissions")
            
    def _execute_trigger_event(self, trigger, value):
        """Execute a trigger event"""
        if self.use_virtual_controller and self.virtual_controller:
            self._execute_virtual_trigger_event(trigger, value)
        else:
            self._execute_keyboard_trigger_event(trigger, value)
            
    def _execute_virtual_trigger_event(self, trigger, value):
        """Execute trigger event using virtual controller"""
        try:
            if virtual_controller_type == "vgamepad" and self.virtual_controller:
                # Map triggers to virtual controller triggers
                if trigger == 'LT':
                    self.virtual_controller.left_trigger_float(value_float=value)
                elif trigger == 'RT':
                    self.virtual_controller.right_trigger_float(value_float=value)
                else:
                    print(f"⚠️  Unknown trigger '{trigger}' - not mapped for virtual controller")
                    return
                # Always call update() to ensure the input is sent to the system
                self.virtual_controller.update()
        except Exception as e:
            print(f"✗ Error with virtual controller trigger {trigger}: {e}")
            print("  Virtual controller may have been disconnected, falling back to keyboard")
            # Disable virtual controller on persistent errors
            self.use_virtual_controller = False
            self.virtual_controller = None
            self._execute_keyboard_trigger_event(trigger, value)
            
    def _execute_keyboard_trigger_event(self, trigger, value):
        """Execute trigger event using keyboard simulation"""
        if not self.keyboard:
            print(f"⚠️  Keyboard controller not available - cannot simulate {trigger}")
            return
            
        # Map triggers to keys with pressure sensitivity simulation
        key = self.key_mappings.get(trigger)
        if key and value > 0.5:  # Threshold for activation
            try:
                self.keyboard.press(key)
                time.sleep(0.05)  # Brief hold
                self.keyboard.release(key)
            except Exception as e:
                print(f"✗ Error executing keyboard trigger event {trigger}: {e}")
                
    def _execute_stick_event(self, stick, value):
        """Execute an analog stick event"""
        if self.use_virtual_controller and self.virtual_controller:
            self._execute_virtual_stick_event(stick, value)
        else:
            self._execute_mouse_stick_event(stick, value)
            
    def _execute_virtual_stick_event(self, stick, value):
        """Execute stick event using virtual controller"""
        try:
            if virtual_controller_type == "vgamepad" and self.virtual_controller:
                x, y = value
                if stick == 'stick_left' or stick == 'left':
                    self.virtual_controller.left_joystick_float(x_value_float=x, y_value_float=y)
                elif stick == 'stick_right' or stick == 'right':
                    self.virtual_controller.right_joystick_float(x_value_float=x, y_value_float=y)
                else:
                    print(f"⚠️  Unknown stick '{stick}' - not mapped for virtual controller")
                    return
                # Always call update() to ensure the input is sent to the system
                self.virtual_controller.update()
        except Exception as e:
            print(f"✗ Error with virtual controller stick {stick}: {e}")
            print("  Virtual controller may have been disconnected, falling back to mouse")
            # Disable virtual controller on persistent errors
            self.use_virtual_controller = False
            self.virtual_controller = None
            self._execute_mouse_stick_event(stick, value)
            
    def _execute_mouse_stick_event(self, stick, value):
        """Execute stick event using mouse simulation"""
        if not self.mouse:
            print(f"⚠️  Mouse controller not available - cannot simulate {stick}")
            return
            
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
            print(f"✗ Error executing mouse stick event {stick}: {e}")
            
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