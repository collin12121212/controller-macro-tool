"""
Macro recording functionality
"""

import time
import threading
import copy

class MacroRecorder:
    def __init__(self, controller_manager):
        self.controller_manager = controller_manager
        self.recording = False
        self.recorded_events = []
        self.start_time = None
        self.last_state = {}
        self.recording_thread = None
        
    def start_recording(self):
        """Start recording controller inputs"""
        self.recording = True
        self.recorded_events = []
        self.start_time = time.time()
        self.last_state = {}
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_loop, daemon=True)
        self.recording_thread.start()
        
        return self.recorded_events
        
    def stop_recording(self):
        """Stop recording and return recorded events"""
        self.recording = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=1)
            
        return self.recorded_events.copy()
        
    def _record_loop(self):
        """Main recording loop"""
        while self.recording:
            try:
                controllers = self.controller_manager.get_connected_controllers()
                
                if controllers:
                    # Record from first controller
                    controller_id = controllers[0]
                    current_state = self.controller_manager.get_controller_state(controller_id)
                    
                    if current_state:
                        self._process_controller_state(current_state)
                        
                time.sleep(1/120)  # High frequency polling for accuracy
            except Exception as e:
                print(f"Error in recording loop: {e}")
                break
                
    def _process_controller_state(self, current_state):
        """Process current controller state and record changes"""
        current_time = time.time() - self.start_time
        
        # Check button changes
        current_buttons = current_state.get('buttons', {})
        last_buttons = self.last_state.get('buttons', {})
        
        for button, pressed in current_buttons.items():
            last_pressed = last_buttons.get(button, False)
            if pressed != last_pressed:
                self._add_event({
                    'type': 'button',
                    'timestamp': current_time,
                    'button': button,
                    'value': pressed,
                    'duration': 0
                })
                
        # Check D-pad changes
        current_dpad = current_state.get('dpad', {})
        last_dpad = self.last_state.get('dpad', {})
        
        for direction, pressed in current_dpad.items():
            last_pressed = last_dpad.get(direction, False)
            if pressed != last_pressed:
                self._add_event({
                    'type': 'dpad',
                    'timestamp': current_time,
                    'button': f'dpad_{direction}',
                    'value': pressed,
                    'duration': 0
                })
                
        # Check analog stick changes (with improved deadzone handling)
        current_sticks = current_state.get('sticks', {})
        last_sticks = self.last_state.get('sticks', {})
        
        deadzone = 0.1
        for stick, (x, y) in current_sticks.items():
            last_pos = last_sticks.get(stick, (0, 0))
            last_x, last_y = last_pos
            
            # Calculate movement deltas
            delta_x = abs(x - last_x)
            delta_y = abs(y - last_y)
            
            # Check if movement is significant (improved handling for simultaneous inputs)
            # Record if either axis moves significantly OR if the overall magnitude changes significantly
            current_magnitude = (x*x + y*y) ** 0.5
            last_magnitude = (last_x*last_x + last_y*last_y) ** 0.5
            magnitude_change = abs(current_magnitude - last_magnitude)
            
            significant_movement = (delta_x > deadzone or delta_y > deadzone or 
                                  magnitude_change > deadzone)
            
            if significant_movement:
                # Validate coordinate ranges before recording
                x_clamped = max(-1.0, min(1.0, x))
                y_clamped = max(-1.0, min(1.0, y))
                
                self._add_event({
                    'type': 'stick',
                    'timestamp': current_time,
                    'button': f'stick_{stick}',
                    'value': (x_clamped, y_clamped),
                    'duration': 0
                })
                
        # Check trigger changes
        current_triggers = current_state.get('triggers', {})
        last_triggers = self.last_state.get('triggers', {})
        
        trigger_threshold = 0.05
        for trigger, value in current_triggers.items():
            last_value = last_triggers.get(trigger, 0)
            
            if abs(value - last_value) > trigger_threshold:
                self._add_event({
                    'type': 'trigger',
                    'timestamp': current_time,
                    'button': trigger,
                    'value': value,
                    'duration': 0
                })
                
        # Update last state
        self.last_state = copy.deepcopy(current_state)
        
    def _add_event(self, event):
        """Add an event to the recorded events list"""
        self.recorded_events.append(event)
        
        # Limit recording length to prevent memory issues
        if len(self.recorded_events) > 10000:  # Max 10k events
            self.recorded_events.pop(0)
            
    def get_recording_status(self):
        """Get current recording status"""
        return {
            'recording': self.recording,
            'event_count': len(self.recorded_events),
            'duration': time.time() - self.start_time if self.start_time else 0
        }