import customtkinter as ctk
import config
from game.blackjack import Blackjack
from game.player import Player
from gui.components import ModernCard, ModernChipDisplay
from gui.modern_stats import ModernStatsWindow
from gui.floating_modals import show_floating_game_result, show_floating_error, show_floating_info

class ResponsiveMainWindow:
    def __init__(self, auth):
        self.auth = auth
        self.user_data = auth.get_user_data()
        
        self.root = ctk.CTk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.minsize(700, 500)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (config.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (config.WINDOW_HEIGHT // 2)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}")
        
        self.game = Blackjack()
        self.player = Player(self.auth.current_user, self.user_data['chips'])
        
        self.dealer_cards = []
        self.player_cards = []
        self.game_in_progress = False
        
        # Bind resize event for responsive behavior
        self.root.bind("<Configure>", self.on_window_resize)
        
        self.setup_ui()
        
        # Force initial layout update
        self.root.after(100, self.update_layout)
        
    def setup_ui(self):
        # Main container with grid layout for responsiveness
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=config.COLORS['primary'])
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure grid weights for responsive behavior
        self.main_container.grid_rowconfigure(1, weight=1)  # Game area expands
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_game_area()
        self.create_controls()
        self.update_display()
        
    def create_header(self):
        # Responsive header
        self.header_frame = ctk.CTkFrame(self.main_container, 
                                       corner_radius=10, 
                                       fg_color=config.COLORS['secondary'])
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        # Configure header grid
        self.header_frame.grid_columnconfigure(1, weight=1)  # Middle expands
        
        # Left: Title
        title_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.title_label = ctk.CTkLabel(title_frame, 
                                      text="🃏 BLACKJACK",
                                      font=('Segoe UI', 18, 'bold'),
                                      text_color=config.COLORS['text_primary'])
        self.title_label.pack()
        
        # Center: User info (responsive)
        user_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        user_frame.grid(row=0, column=1, sticky="", padx=10, pady=10)
        
        self.user_label = ctk.CTkLabel(user_frame,
                                     text=f"👤 {self.auth.current_user}",
                                     font=config.FONTS['body'],
                                     text_color=config.COLORS['text_primary'])
        self.user_label.pack()
        
        # Right: Chips and stats
        controls_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        
        self.chip_display = ModernChipDisplay(controls_frame, self.player.chips)
        self.chip_display.pack(side="left", padx=(0, 5))
        
        self.stats_btn = ctk.CTkButton(controls_frame, 
                                     text="📊",
                                     command=self.show_stats,
                                     width=35,
                                     height=35,
                                     font=('Segoe UI', 12),
                                     fg_color=config.COLORS['warning'],
                                     hover_color=config.COLORS['warning'])
        self.stats_btn.pack(side="left")
        
    def create_game_area(self):
        # Responsive game area
        self.game_frame = ctk.CTkFrame(self.main_container, 
                                     corner_radius=15, 
                                     fg_color=config.COLORS['table_green'])
        self.game_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure game area grid
        self.game_frame.grid_rowconfigure(0, weight=1)  # Dealer area
        self.game_frame.grid_rowconfigure(1, weight=1)  # Player area
        self.game_frame.grid_columnconfigure(0, weight=1)
        
        # Dealer section
        self.dealer_section = ctk.CTkFrame(self.game_frame, 
                                         corner_radius=10, 
                                         fg_color=config.COLORS['dealer_area'])
        self.dealer_section.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Dealer header
        dealer_header = ctk.CTkFrame(self.dealer_section, fg_color="transparent")
        dealer_header.pack(fill="x", padx=10, pady=(8, 5))
        
        dealer_label = ctk.CTkLabel(dealer_header,
                                  text="🎩 DEALER",
                                  font=config.FONTS['body'],
                                  text_color=config.COLORS['text_primary'])
        dealer_label.pack(side="left")
        
        self.dealer_score_label = ctk.CTkLabel(dealer_header,
                                             text="Score: 0",
                                             font=config.FONTS['body'],
                                             text_color=config.COLORS['text_secondary'])
        self.dealer_score_label.pack(side="right")
        
        # Dealer cards (scrollable for many cards)
        self.dealer_cards_container = ctk.CTkScrollableFrame(self.dealer_section, 
                                                           orientation="horizontal",
                                                           height=120,
                                                           fg_color="transparent")
        self.dealer_cards_container.pack(fill="x", padx=10, pady=(0, 8))
        
        # Player section
        self.player_section = ctk.CTkFrame(self.game_frame, 
                                         corner_radius=10, 
                                         fg_color=config.COLORS['player_area'])
        self.player_section.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # Player header
        player_header = ctk.CTkFrame(self.player_section, fg_color="transparent")
        player_header.pack(fill="x", padx=10, pady=(8, 5))
        
        player_label = ctk.CTkLabel(player_header,
                                  text="🎮 PLAYER",
                                  font=config.FONTS['body'],
                                  text_color=config.COLORS['text_primary'])
        player_label.pack(side="left")
        
        self.player_score_label = ctk.CTkLabel(player_header,
                                             text="Score: 0",
                                             font=config.FONTS['body'],
                                             text_color=config.COLORS['text_secondary'])
        self.player_score_label.pack(side="right")
        
        # Player cards (scrollable for many cards)
        self.player_cards_container = ctk.CTkScrollableFrame(self.player_section, 
                                                           orientation="horizontal",
                                                           height=120,
                                                           fg_color="transparent")
        self.player_cards_container.pack(fill="x", padx=10, pady=(0, 8))
        
    def create_controls(self):
        # Responsive controls
        self.controls_frame = ctk.CTkFrame(self.main_container, 
                                         corner_radius=10, 
                                         fg_color=config.COLORS['secondary'])
        self.controls_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        # Configure controls grid for responsiveness
        self.controls_frame.grid_columnconfigure(1, weight=1)  # Middle section expands
        
        # Left: Betting controls
        bet_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        bet_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        bet_label = ctk.CTkLabel(bet_frame,
                               text="💰 Bet",
                               font=config.FONTS['small'],
                               text_color=config.COLORS['text_primary'])
        bet_label.pack()
        
        self.bet_var = ctk.IntVar(value=10)
        self.bet_slider = ctk.CTkSlider(bet_frame,
                                      from_=1,
                                      to=min(self.player.chips, 100),
                                      variable=self.bet_var,
                                      width=120,
                                      height=16,
                                      command=self.update_bet_display)
        self.bet_slider.pack(pady=3)
        
        self.bet_amount_label = ctk.CTkLabel(bet_frame,
                                           text=f"${self.bet_var.get()}",
                                           font=config.FONTS['small'],
                                           text_color=config.COLORS['chips_gold'])
        self.bet_amount_label.pack()
        
        # Right: Game buttons (responsive layout)
        self.buttons_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        
        # Create responsive button layout
        self.create_responsive_buttons()
        
    def create_responsive_buttons(self):
        # Clear existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
            
        # Get current window width to determine layout
        window_width = self.root.winfo_width()
        
        if window_width < 800:
            # Vertical layout for narrow windows
            self.deal_btn = ctk.CTkButton(self.buttons_frame, 
                                        text="🎴 Deal",
                                        command=self.deal_cards,
                                        width=70,
                                        height=30,
                                        font=config.FONTS['small'],
                                        fg_color=config.COLORS['accent'])
            self.deal_btn.pack(pady=1)
            
            self.hit_btn = ctk.CTkButton(self.buttons_frame, 
                                       text="👆 Hit",
                                       command=self.hit,
                                       width=70,
                                       height=30,
                                       font=config.FONTS['small'],
                                       fg_color=config.COLORS['success'],
                                       state="disabled")
            self.hit_btn.pack(pady=1)
            
            self.stand_btn = ctk.CTkButton(self.buttons_frame, 
                                         text="✋ Stand",
                                         command=self.stand,
                                         width=70,
                                         height=30,
                                         font=config.FONTS['small'],
                                         fg_color=config.COLORS['warning'],
                                         state="disabled")
            self.stand_btn.pack(pady=1)
            
            self.double_btn = ctk.CTkButton(self.buttons_frame, 
                                          text="⚡ Double",
                                          command=self.double_down,
                                          width=70,
                                          height=30,
                                          font=config.FONTS['small'],
                                          fg_color=config.COLORS['danger'],
                                          state="disabled")
            self.double_btn.pack(pady=1)
        else:
            # Horizontal layout for wider windows
            button_row = ctk.CTkFrame(self.buttons_frame, fg_color="transparent")
            button_row.pack()
            
            self.deal_btn = ctk.CTkButton(button_row, 
                                        text="🎴 Deal",
                                        command=self.deal_cards,
                                        width=70,
                                        height=35,
                                        font=config.FONTS['small'],
                                        fg_color=config.COLORS['accent'])
            self.deal_btn.pack(side="left", padx=2)
            
            self.hit_btn = ctk.CTkButton(button_row, 
                                       text="👆 Hit",
                                       command=self.hit,
                                       width=70,
                                       height=35,
                                       font=config.FONTS['small'],
                                       fg_color=config.COLORS['success'],
                                       state="disabled")
            self.hit_btn.pack(side="left", padx=2)
            
            self.stand_btn = ctk.CTkButton(button_row, 
                                         text="✋ Stand",
                                         command=self.stand,
                                         width=70,
                                         height=35,
                                         font=config.FONTS['small'],
                                         fg_color=config.COLORS['warning'],
                                         state="disabled")
            self.stand_btn.pack(side="left", padx=2)
            
            self.double_btn = ctk.CTkButton(button_row, 
                                          text="⚡ Double",
                                          command=self.double_down,
                                          width=70,
                                          height=35,
                                          font=config.FONTS['small'],
                                          fg_color=config.COLORS['danger'],
                                          state="disabled")
            self.double_btn.pack(side="left", padx=2)
    
    def on_window_resize(self, event):
        # Only respond to root window resize events
        if event.widget == self.root:
            self.root.after_idle(self.update_layout)
    
    def update_layout(self):
        # Update button layout based on current window size
        self.create_responsive_buttons()
        
        # Update card sizes based on window size
        window_width = self.root.winfo_width()
        if window_width < 800:
            # Smaller cards for narrow windows
            config.CARD_WIDTH = 60
            config.CARD_HEIGHT = 85
        else:
            # Normal card size
            config.CARD_WIDTH = 70
            config.CARD_HEIGHT = 100
            
        # Refresh card display if cards are present
        if self.dealer_cards or self.player_cards:
            self.display_cards()
    
    def update_bet_display(self, value):
        self.bet_amount_label.configure(text=f"${int(value)}")
        
    def get_bet_amount(self):
        return int(self.bet_var.get())
        
    def deal_cards(self):
        bet_amount = self.get_bet_amount()
        if not self.player.place_bet(bet_amount):
            show_floating_error(self.root, "Insufficient Chips", "You don't have enough chips for this bet!")
            return
            
        self.game_in_progress = True
        self.game.start_game()
        
        self.clear_cards()
        self.display_cards()
        self.update_display()
        
        if self.game.blackjack:
            self.root.after(1000, self.end_game)
        else:
            self.enable_game_buttons()
            
    def hit(self):
        self.game.hit()
        self.display_cards()
        self.update_display()
        
        if self.game.gameOver:
            self.root.after(500, self.end_game)
            
    def stand(self):
        self.game.stand()
        self.display_cards()
        self.update_display()
        self.root.after(500, self.end_game)
        
    def double_down(self):
        if self.player.chips >= self.player.current_bet:
            self.player.chips -= self.player.current_bet
            self.player.current_bet *= 2
            self.game.hit()
            if not self.game.gameOver:
                self.game.stand()
            self.display_cards()
            self.update_display()
            self.root.after(500, self.end_game)
        else:
            show_floating_error(self.root, "Insufficient Chips", "You don't have enough chips to double down!")
            
    def clear_cards(self):
        for widget in self.dealer_cards_container.winfo_children():
            widget.destroy()
        for widget in self.player_cards_container.winfo_children():
            widget.destroy()
        self.dealer_cards = []
        self.player_cards = []
        
    def display_cards(self):
        self.clear_cards()
        
        # Dealer cards
        for i, card in enumerate(self.game.dealerHand):
            hidden = i == 1 and self.game.currentTurn == "Player" and not self.game.gameOver
            card_widget = ModernCard(self.dealer_cards_container, card, hidden)
            card_widget.pack(side="left", padx=3, pady=5)
            self.dealer_cards.append(card_widget)
            
        # Player cards
        for card in self.game.playerHand:
            card_widget = ModernCard(self.player_cards_container, card)
            card_widget.pack(side="left", padx=3, pady=5)
            self.player_cards.append(card_widget)
            
    def update_display(self):
        # Update scores with color coding
        if self.game.currentTurn == "Player" and not self.game.gameOver:
            dealer_visible = self.game.dealerHand[0].get_value() if self.game.dealerHand else 0
            self.dealer_score_label.configure(text=f"Score: {dealer_visible}+")
        else:
            score_color = config.COLORS['text_secondary']
            if self.game.dealerScore > 21:
                score_color = config.COLORS['danger']
            elif self.game.dealerScore == 21:
                score_color = config.COLORS['success']
            self.dealer_score_label.configure(text=f"Score: {self.game.dealerScore}",
                                            text_color=score_color)
            
        # Player score with color coding
        score_color = config.COLORS['text_secondary']
        if self.game.playerScore > 21:
            score_color = config.COLORS['danger']
        elif self.game.playerScore == 21:
            score_color = config.COLORS['success']
        self.player_score_label.configure(text=f"Score: {self.game.playerScore}",
                                        text_color=score_color)
        
        # Update chip display
        self.chip_display.update_chips(self.player.chips)
        
        # Update bet slider max
        if not self.game_in_progress:
            max_bet = min(self.player.chips, 100)
            self.bet_slider.configure(to=max_bet)
            if self.bet_var.get() > max_bet:
                self.bet_var.set(max_bet)
        
    def enable_game_buttons(self):
        self.deal_btn.configure(state="disabled")
        self.hit_btn.configure(state="normal")
        self.stand_btn.configure(state="normal")
        
        can_double = (len(self.game.playerHand) == 2 and 
                     self.player.chips >= self.player.current_bet)
        self.double_btn.configure(state="normal" if can_double else "disabled")
        
    def disable_game_buttons(self):
        self.deal_btn.configure(state="normal")
        self.hit_btn.configure(state="disabled")
        self.stand_btn.configure(state="disabled")
        self.double_btn.configure(state="disabled")
        
    def end_game(self):
        self.game_in_progress = False
        self.disable_game_buttons()
        
        # Handle winnings
        if self.game.result == "win":
            multiplier = 0.5 if self.game.blackjack else 1
            self.player.win_bet(multiplier)
        elif self.game.result == "lose":
            self.player.lose_bet()
        else:
            self.player.draw_bet()
            
        # Show floating modal instead of full-screen modal
        show_floating_game_result(self.root, self.game.result, self.game.blackjack)
        
        self.save_game_stats()
        self.update_display()
        
        # Check if player is out of chips
        if self.player.chips <= 0:
            show_floating_info(self.root, "Game Over", "You're out of chips! Thanks for playing!")
            self.root.quit()
            
    def save_game_stats(self):
        user_data = {
            'chips': self.player.chips,
            'games_played': self.user_data['games_played'] + 1
        }
        
        if self.game.result == "win":
            user_data['games_won'] = self.user_data['games_won'] + 1
        elif self.game.result == "lose":
            user_data['games_lost'] = self.user_data['games_lost'] + 1
        else:
            user_data['games_drawn'] = self.user_data['games_drawn'] + 1
            
        # Refresh session and save data
        if self.auth.refresh_session():
            self.auth.update_user_data(user_data)
            self.user_data.update(user_data)
        else:
            show_floating_error(self.root, "Session Expired", "Please login again to save your progress")
            self.logout_and_return_to_login()
        
    def show_stats(self):
        stats_window = ModernStatsWindow(self.root, self.user_data)
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def logout_and_return_to_login(self):
        """Logout and return to login screen"""
        self.auth.logout()
        self.root.destroy()
        from gui.modern_login import ModernLoginWindow
        login = ModernLoginWindow()
        login.run()
        
    def on_closing(self):
        self.save_game_stats()
        self.auth.logout()
        self.root.destroy()

if __name__ == "__main__":
    from utils.auth import UserAuth
    auth = UserAuth()
    auth.current_user = "test"
    game = ResponsiveMainWindow(auth)
    game.run()