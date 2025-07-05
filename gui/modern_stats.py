import customtkinter as ctk
import config

class ModernStatsWindow:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title("📊 Player Statistics")
        self.window.geometry("600x700")
        self.window.resizable(True, True)
        self.window.minsize(500, 600)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (700 // 2)
        self.window.geometry(f"600x700+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['secondary'])
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(header_frame,
                                 text="📊 PLAYER STATISTICS",
                                 font=config.FONTS['title'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(pady=30)
        
        # Stats grid
        stats_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['secondary'])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Create stats grid
        self.create_stats_grid(stats_frame)
        
        # Performance section
        performance_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['primary'])
        performance_frame.pack(fill="x", pady=(0, 20))
        
        perf_title = ctk.CTkLabel(performance_frame,
                                text="📈 PERFORMANCE ANALYSIS",
                                font=config.FONTS['subtitle'],
                                text_color=config.COLORS['text_primary'])
        perf_title.pack(pady=(20, 10))
        
        self.create_performance_section(performance_frame)
        
        # Achievements section
        achievements_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['table_green'])
        achievements_frame.pack(fill="x", pady=(0, 20))
        
        ach_title = ctk.CTkLabel(achievements_frame,
                               text="🏆 ACHIEVEMENTS",
                               font=config.FONTS['subtitle'],
                               text_color=config.COLORS['text_primary'])
        ach_title.pack(pady=(20, 10))
        
        self.create_achievements_section(achievements_frame)
        
        # Close button
        close_btn = ctk.CTkButton(main_frame,
                                text="✖️ Close",
                                command=self.window.destroy,
                                width=200,
                                height=45,
                                font=config.FONTS['button'],
                                fg_color=config.COLORS['danger'],
                                hover_color=config.COLORS['danger'],
                                corner_radius=8)
        close_btn.pack(pady=20)
        
    def create_stats_grid(self, parent):
        # Grid container
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(padx=30, pady=30)
        
        # Row 1
        row1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        
        self.create_stat_card(row1, "💰", "Current Chips", f"${self.user_data['chips']:,}", config.COLORS['chips_gold'])
        self.create_stat_card(row1, "🎮", "Games Played", str(self.user_data['games_played']), config.COLORS['accent'])
        
        # Row 2
        row2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 15))
        
        self.create_stat_card(row2, "🏆", "Games Won", str(self.user_data['games_won']), config.COLORS['success'])
        self.create_stat_card(row2, "😔", "Games Lost", str(self.user_data['games_lost']), config.COLORS['danger'])
        
        # Row 3
        row3 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row3.pack(fill="x")
        
        self.create_stat_card(row3, "🤝", "Games Drawn", str(self.user_data['games_drawn']), config.COLORS['warning'])
        
        if self.user_data['games_played'] > 0:
            win_rate = (self.user_data['games_won'] / self.user_data['games_played']) * 100
            self.create_stat_card(row3, "📊", "Win Rate", f"{win_rate:.1f}%", config.COLORS['accent'])
        else:
            self.create_stat_card(row3, "📊", "Win Rate", "0.0%", config.COLORS['text_muted'])
            
    def create_stat_card(self, parent, icon, label, value, color):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color=config.COLORS['primary'])
        card.pack(side="left", fill="x", expand=True, padx=5)
        
        icon_label = ctk.CTkLabel(card,
                                text=icon,
                                font=('Segoe UI', 24),
                                text_color=color)
        icon_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(card,
                                 text=value,
                                 font=('Segoe UI', 20, 'bold'),
                                 text_color=config.COLORS['text_primary'])
        value_label.pack(pady=(0, 5))
        
        label_widget = ctk.CTkLabel(card,
                                  text=label,
                                  font=config.FONTS['small'],
                                  text_color=config.COLORS['text_secondary'])
        label_widget.pack(pady=(0, 15))
        
    def create_performance_section(self, parent):
        perf_container = ctk.CTkFrame(parent, fg_color="transparent")
        perf_container.pack(padx=30, pady=(0, 20))
        
        if self.user_data['games_played'] > 0:
            # Net profit/loss
            net_chips = self.user_data['chips'] - config.STARTING_CHIPS
            profit_color = config.COLORS['success'] if net_chips >= 0 else config.COLORS['danger']
            profit_text = f"+${net_chips:,}" if net_chips >= 0 else f"-${abs(net_chips):,}"
            
            profit_frame = ctk.CTkFrame(perf_container, corner_radius=10, fg_color=config.COLORS['secondary'])
            profit_frame.pack(fill="x", pady=(0, 10))
            
            profit_label = ctk.CTkLabel(profit_frame,
                                      text=f"💵 Net Profit/Loss: {profit_text}",
                                      font=config.FONTS['subtitle'],
                                      text_color=profit_color)
            profit_label.pack(pady=15)
            
            # Performance rating
            win_rate = (self.user_data['games_won'] / self.user_data['games_played']) * 100
            
            if win_rate >= 75:
                rating = "🌟 LEGENDARY"
                rating_color = config.COLORS['chips_gold']
            elif win_rate >= 60:
                rating = "⭐ EXPERT"
                rating_color = config.COLORS['success']
            elif win_rate >= 45:
                rating = "👍 GOOD"
                rating_color = config.COLORS['accent']
            elif win_rate >= 30:
                rating = "📈 LEARNING"
                rating_color = config.COLORS['warning']
            else:
                rating = "🎯 BEGINNER"
                rating_color = config.COLORS['text_secondary']
                
            rating_frame = ctk.CTkFrame(perf_container, corner_radius=10, fg_color=config.COLORS['secondary'])
            rating_frame.pack(fill="x")
            
            rating_label = ctk.CTkLabel(rating_frame,
                                      text=f"Player Rating: {rating}",
                                      font=config.FONTS['subtitle'],
                                      text_color=rating_color)
            rating_label.pack(pady=15)
        else:
            no_data_label = ctk.CTkLabel(perf_container,
                                       text="🎮 Play some games to see your performance!",
                                       font=config.FONTS['body'],
                                       text_color=config.COLORS['text_secondary'])
            no_data_label.pack(pady=20)
            
    def create_achievements_section(self, parent):
        achievements_container = ctk.CTkFrame(parent, fg_color="transparent")
        achievements_container.pack(padx=30, pady=(0, 20))
        
        achievements = self.get_achievements()
        
        if achievements:
            # Create grid of achievements
            for i, achievement in enumerate(achievements):
                if i % 2 == 0:  # Start new row
                    row = ctk.CTkFrame(achievements_container, fg_color="transparent")
                    row.pack(fill="x", pady=5)
                    
                ach_card = ctk.CTkFrame(row, corner_radius=8, fg_color=config.COLORS['secondary'])
                ach_card.pack(side="left", fill="x", expand=True, padx=5)
                
                ach_label = ctk.CTkLabel(ach_card,
                                       text=achievement,
                                       font=config.FONTS['body'],
                                       text_color=config.COLORS['chips_gold'])
                ach_label.pack(pady=10)
        else:
            no_ach_label = ctk.CTkLabel(achievements_container,
                                      text="🌟 Start playing to unlock achievements!",
                                      font=config.FONTS['body'],
                                      text_color=config.COLORS['text_secondary'])
            no_ach_label.pack(pady=20)
            
    def get_achievements(self):
        achievements = []
        
        # Game count achievements
        if self.user_data['games_played'] >= 1:
            achievements.append("🎮 First Game")
        if self.user_data['games_played'] >= 10:
            achievements.append("🔥 Veteran Player")
        if self.user_data['games_played'] >= 50:
            achievements.append("⭐ Blackjack Master")
        if self.user_data['games_played'] >= 100:
            achievements.append("💎 Century Club")
            
        # Win achievements
        if self.user_data['games_won'] >= 5:
            achievements.append("🏆 Winner")
        if self.user_data['games_won'] >= 20:
            achievements.append("👑 Champion")
        if self.user_data['games_won'] >= 50:
            achievements.append("🎯 Sharpshooter")
            
        # Chip achievements
        if self.user_data['chips'] >= 2000:
            achievements.append("💰 High Roller")
        if self.user_data['chips'] >= 5000:
            achievements.append("💎 Millionaire")
        if self.user_data['chips'] >= 10000:
            achievements.append("🏦 Casino Crusher")
            
        # Win rate achievements
        if self.user_data['games_played'] > 0:
            win_rate = (self.user_data['games_won'] / self.user_data['games_played']) * 100
            if win_rate >= 60:
                achievements.append("🎯 Sharp Player")
            if win_rate >= 75:
                achievements.append("🧠 Card Counter")
            if win_rate >= 90:
                achievements.append("🌟 Legendary")
                
        return achievements

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    
    sample_data = {
        'chips': 2500,
        'games_played': 35,
        'games_won': 22,
        'games_lost': 11,
        'games_drawn': 2
    }
    
    stats = ModernStatsWindow(root, sample_data)
    root.mainloop()