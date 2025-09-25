"""
Modern Theme Manager for Controller Macro Tool
Provides a professional dark theme with accent colors and animations
"""

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self):
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a1a',      # Deep dark
            'bg_secondary': '#2d2d30',     # Secondary dark
            'bg_tertiary': '#3e3e42',      # Tertiary background
            'accent_blue': '#0078d4',      # Primary accent
            'accent_blue_hover': '#106ebe', # Hover accent
            'accent_purple': '#6b46c1',    # Purple accent
            'success': '#00b56a',          # Success green
            'warning': '#ff8c00',          # Warning orange
            'error': '#e74856',            # Error red
            'text_primary': '#ffffff',     # Primary text
            'text_secondary': '#cccccc',   # Secondary text
            'text_muted': '#999999',       # Muted text
            'border': '#555555',           # Border color
            'border_active': '#0078d4',    # Active border
        }
        
        self.fonts = {
            'default': ('Segoe UI', 10),
            'heading': ('Segoe UI', 12, 'bold'),
            'large': ('Segoe UI', 14, 'bold'),
            'small': ('Segoe UI', 8),
            'mono': ('Consolas', 10),
        }
        
    def apply_theme(self, root):
        """Apply modern dark theme to the application"""
        style = ttk.Style()
        
        # Use a modern theme as base
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Configure root window
        root.configure(bg=self.colors['bg_primary'])
        
        # Configure ttk styles
        self._configure_ttk_styles(style)
        
        return style
        
    def _configure_ttk_styles(self, style):
        """Configure TTK widget styles"""
        
        # Frame styles
        style.configure('TFrame', 
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        # Label styles
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['default'])
        
        style.configure('Heading.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['heading'])
        
        style.configure('Muted.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_muted'],
                       font=self.fonts['small'])
        
        # Button styles
        style.configure('TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       focuscolor='none',
                       font=self.fonts['default'])
        
        style.map('TButton',
                 background=[('active', self.colors['accent_blue_hover']),
                           ('pressed', self.colors['accent_blue'])],
                 foreground=[('active', self.colors['text_primary'])])
        
        # Primary button style
        style.configure('Primary.TButton',
                       background=self.colors['accent_blue'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       font=self.fonts['default'])
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['accent_blue_hover']),
                           ('pressed', self.colors['accent_blue'])],
                 foreground=[('active', self.colors['text_primary'])])
        
        # Success button style
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0)
        
        style.map('Success.TButton',
                 background=[('active', '#00a85d')])
        
        # Danger button style
        style.configure('Danger.TButton',
                       background=self.colors['error'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0)
        
        style.map('Danger.TButton',
                 background=[('active', '#d13438')])
        
        # Entry styles
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_tertiary'],
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       insertcolor=self.colors['text_primary'],
                       font=self.fonts['default'])
        
        style.map('TEntry',
                 bordercolor=[('focus', self.colors['border_active'])])
        
        # Listbox style (for macro list)
        style.configure('TListbox',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       selectbackground=self.colors['accent_blue'],
                       selectforeground=self.colors['text_primary'],
                       borderwidth=1,
                       font=self.fonts['default'])
        
        # Treeview styles (for macro editor)
        style.configure('Treeview',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=1,
                       font=self.fonts['default'])
        
        style.configure('Treeview.Heading',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       font=self.fonts['heading'])
        
        style.map('Treeview',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        # Notebook styles
        style.configure('TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       font=self.fonts['default'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['bg_secondary'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        # Scale/Progressbar styles
        style.configure('TScale',
                       background=self.colors['bg_primary'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent_blue'],
                       darkcolor=self.colors['accent_blue'])
        
        style.configure('TProgressbar',
                       background=self.colors['accent_blue'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent_blue'],
                       darkcolor=self.colors['accent_blue'])
        
        # Paned window
        style.configure('TPanedwindow',
                       background=self.colors['bg_primary'])
        
        # Separator
        style.configure('TSeparator',
                       background=self.colors['border'])
        
    def create_gradient_button(self, parent, text, command=None, style='Primary'):
        """Create a modern button with gradient-like appearance"""
        btn = ttk.Button(parent, text=text, command=command, style=f'{style}.TButton')
        
        # Add hover effects
        def on_enter(event):
            event.widget.configure(cursor='hand2')
        
        def on_leave(event):
            event.widget.configure(cursor='')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
        
    def create_card_frame(self, parent, **kwargs):
        """Create a card-style frame with modern appearance"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
        
    def get_color(self, color_name):
        """Get a color from the theme"""
        return self.colors.get(color_name, '#ffffff')
        
    def get_font(self, font_name):
        """Get a font from the theme"""
        return self.fonts.get(font_name, ('Arial', 10))