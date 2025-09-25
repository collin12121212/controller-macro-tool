"""
Modern Notification System for Controller Macro Tool
Provides toast-style notifications and status updates
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class NotificationManager:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.notifications = []
        self.notification_frame = None
        
    def show_notification(self, message, notification_type="info", duration=3000):
        """Show a toast-style notification"""
        # Create notification frame if it doesn't exist
        if not self.notification_frame:
            self.setup_notification_area()
            
        notification = self.create_notification(message, notification_type)
        self.notifications.append(notification)
        
        # Auto-hide after duration
        if duration > 0:
            threading.Timer(duration / 1000, lambda: self.hide_notification(notification)).start()
        
        return notification
        
    def setup_notification_area(self):
        """Setup the notification display area"""
        self.notification_frame = tk.Frame(
            self.parent,
            bg=self.theme_manager.get_color('bg_primary')
        )
        self.notification_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
        
    def create_notification(self, message, notification_type):
        """Create a single notification widget"""
        # Color mapping for notification types
        colors = {
            'info': self.theme_manager.get_color('accent_blue'),
            'success': self.theme_manager.get_color('success'),
            'warning': self.theme_manager.get_color('warning'),
            'error': self.theme_manager.get_color('error')
        }
        
        # Icons for notification types
        icons = {
            'info': 'ℹ',
            'success': '✓',
            'warning': '⚠',
            'error': '✗'
        }
        
        # Create notification container
        notification_container = tk.Frame(
            self.notification_frame,
            bg=colors.get(notification_type, colors['info']),
            relief='flat',
            bd=0
        )
        notification_container.pack(fill=tk.X, pady=2)
        
        # Add inner frame for content
        inner_frame = tk.Frame(
            notification_container,
            bg=self.theme_manager.get_color('bg_secondary'),
            relief='flat',
            bd=1
        )
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Content frame
        content_frame = tk.Frame(
            inner_frame,
            bg=self.theme_manager.get_color('bg_secondary')
        )
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Icon
        icon_label = tk.Label(
            content_frame,
            text=icons.get(notification_type, icons['info']),
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=colors.get(notification_type, colors['info']),
            font=self.theme_manager.get_font('default'),
            width=2
        )
        icon_label.pack(side=tk.LEFT)
        
        # Message
        message_label = tk.Label(
            content_frame,
            text=message,
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('text_primary'),
            font=self.theme_manager.get_font('small'),
            wraplength=250,
            justify=tk.LEFT
        )
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Close button
        close_btn = tk.Button(
            content_frame,
            text='×',
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('text_muted'),
            font=('Arial', 12, 'bold'),
            relief='flat',
            bd=0,
            width=2,
            cursor='hand2',
            command=lambda: self.hide_notification(notification_container)
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Add animation effect
        self.animate_notification_in(notification_container)
        
        return notification_container
        
    def hide_notification(self, notification):
        """Hide a specific notification"""
        if notification and notification in self.notifications:
            try:
                self.animate_notification_out(notification)
                self.notifications.remove(notification)
            except:
                pass
                
    def animate_notification_in(self, notification):
        """Animate notification sliding in"""
        # Simple fade-in effect
        notification.configure(bg=self.theme_manager.get_color('bg_secondary'))
        
    def animate_notification_out(self, notification):
        """Animate notification sliding out"""
        try:
            notification.destroy()
        except:
            pass
            
    def clear_all_notifications(self):
        """Clear all notifications"""
        for notification in self.notifications.copy():
            self.hide_notification(notification)
            
    def show_status_update(self, message, status_type="info"):
        """Show a status update that persists until replaced"""
        return self.show_notification(message, status_type, duration=0)

class StatusManager:
    """Manages application status display"""
    
    def __init__(self, status_label, theme_manager):
        self.status_label = status_label
        self.theme_manager = theme_manager
        self.current_status = "Ready"
        
    def update_status(self, message, status_type="info"):
        """Update the main status bar"""
        colors = {
            'info': self.theme_manager.get_color('text_primary'),
            'success': self.theme_manager.get_color('success'),
            'warning': self.theme_manager.get_color('warning'),
            'error': self.theme_manager.get_color('error'),
            'recording': self.theme_manager.get_color('accent_blue'),
            'playing': self.theme_manager.get_color('success')
        }
        
        self.current_status = message
        if hasattr(self.status_label, 'configure'):
            self.status_label.configure(
                text=message,
                foreground=colors.get(status_type, colors['info'])
            )
            
    def get_current_status(self):
        """Get the current status message"""
        return self.current_status
        
    def flash_status(self, message, status_type="info", duration=2000):
        """Flash a temporary status message"""
        original_status = self.current_status
        self.update_status(message, status_type)
        
        # Restore original status after duration
        threading.Timer(duration / 1000, lambda: self.update_status(original_status)).start()