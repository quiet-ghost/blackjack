import tkinter as tk
from tkinter import ttk
import config

class StatsWindow:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        
        self.window = tk.Toplevel(parent)
        self.window.title("Player Statistics")
        self.window.geometry("400x500")
        self.window.configure(bg=config.COLORS['background'])
        self.window.resizable(False, False)
        self.window.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.window, bg=config.COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="📊 PLAYER STATISTICS 📊", 
                              font=config.FONTS['title'],
                              bg=config.COLORS['background'], 
                              fg=config.COLORS['text_primary'])
        title_label.pack(pady=20)
        
        stats_frame = tk.Frame(main_frame, bg=config.COLORS['background'])
        stats_frame.pack(expand=True, fill='both')
        
        self.create_stat_row(stats_frame, "Current Chips:", f"${self.user_data['chips']}")
        self.create_stat_row(stats_frame, "Games Played:", str(self.user_data['games_played']))
        self.create_stat_row(stats_frame, "Games Won:", str(self.user_data['games_won']))
        self.create_stat_row(stats_frame, "Games Lost:", str(self.user_data['games_lost']))
        self.create_stat_row(stats_frame, "Games Drawn:", str(self.user_data['games_drawn']))
        
        if self.user_data['games_played'] > 0:
            win_rate = (self.user_data['games_won'] / self.user_data['games_played']) * 100
            self.create_stat_row(stats_frame, "Win Rate:", f"{win_rate:.1f}%")
            
            net_chips = self.user_data['chips'] - config.STARTING_CHIPS
            profit_color = config.COLORS['text_primary'] if net_chips >= 0 else 'red'
            profit_text = f"+${net_chips}" if net_chips >= 0 else f"-${abs(net_chips)}"
            self.create_stat_row(stats_frame, "Net Profit/Loss:", profit_text, profit_color)
        
        separator = tk.Frame(stats_frame, height=2, bg=config.COLORS['text_secondary'])
        separator.pack(fill='x', pady=20)
        
        achievements_label = tk.Label(stats_frame, text="🏆 ACHIEVEMENTS", 
                                    font=config.FONTS['subtitle'],
                                    bg=config.COLORS['background'], 
                                    fg=config.COLORS['text_primary'])
        achievements_label.pack(pady=10)
        
        achievements_frame = tk.Frame(stats_frame, bg=config.COLORS['background'])
        achievements_frame.pack(fill='x')
        
        self.show_achievements(achievements_frame)
        
        close_btn = tk.Button(main_frame, text="Close", command=self.window.destroy,
                             font=config.FONTS['button'], width=10,
                             bg=config.COLORS['button_bg'], fg=config.COLORS['button_text'])
        close_btn.pack(pady=20)
        
    def create_stat_row(self, parent, label, value, value_color=None):
        row_frame = tk.Frame(parent, bg=config.COLORS['background'])
        row_frame.pack(fill='x', pady=5)
        
        label_widget = tk.Label(row_frame, text=label, font=config.FONTS['body'],
                               bg=config.COLORS['background'], fg=config.COLORS['text_secondary'])
        label_widget.pack(side='left')
        
        value_widget = tk.Label(row_frame, text=value, font=config.FONTS['subtitle'],
                               bg=config.COLORS['background'], 
                               fg=value_color or config.COLORS['text_primary'])
        value_widget.pack(side='right')
        
    def show_achievements(self, parent):
        achievements = []
        
        if self.user_data['games_played'] >= 1:
            achievements.append("🎮 First Game")
        if self.user_data['games_played'] >= 10:
            achievements.append("🔥 Veteran Player")
        if self.user_data['games_played'] >= 50:
            achievements.append("⭐ Blackjack Master")
            
        if self.user_data['games_won'] >= 5:
            achievements.append("🏆 Winner")
        if self.user_data['games_won'] >= 20:
            achievements.append("👑 Champion")
            
        if self.user_data['chips'] >= 2000:
            achievements.append("💰 High Roller")
        if self.user_data['chips'] >= 5000:
            achievements.append("💎 Millionaire")
            
        if self.user_data['games_played'] > 0:
            win_rate = (self.user_data['games_won'] / self.user_data['games_played']) * 100
            if win_rate >= 60:
                achievements.append("🎯 Sharp Player")
            if win_rate >= 75:
                achievements.append("🧠 Card Counter")
                
        if not achievements:
            achievements.append("🌟 New Player")
            
        for achievement in achievements:
            achievement_label = tk.Label(parent, text=achievement, font=config.FONTS['body'],
                                       bg=config.COLORS['background'], fg=config.COLORS['chips_gold'])
            achievement_label.pack(anchor='w', pady=2)