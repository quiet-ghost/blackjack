import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
WINDOW_TITLE = "🃏 Blackjack Casino"

COLORS = {
    'primary': '#1a1a1a',
    'secondary': '#2b2b2b', 
    'accent': '#00d4aa',
    'accent_hover': '#00b894',
    'success': '#00b894',
    'warning': '#fdcb6e',
    'danger': '#e17055',
    'card_bg': '#ffffff',
    'card_shadow': '#00000020',
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'text_muted': '#6c757d',
    'chips_gold': '#f39c12',
    'dealer_area': '#2d3436',
    'player_area': '#636e72',
    'table_green': '#0d7377'
}

FONTS = {
    'title': ('Segoe UI', 28, 'bold'),
    'subtitle': ('Segoe UI', 18, 'bold'),
    'body': ('Segoe UI', 14),
    'button': ('Segoe UI', 16, 'bold'),
    'card': ('Segoe UI', 24, 'bold'),
    'small': ('Segoe UI', 12)
}

CARD_WIDTH = 70
CARD_HEIGHT = 100
CARD_SPACING = 15
CARD_CORNER_RADIUS = 12

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_CORNER_RADIUS = 8

STARTING_CHIPS = 1000

ANIMATIONS = {
    'card_deal_delay': 200,
    'button_hover_time': 150,
    'fade_duration': 300
}
