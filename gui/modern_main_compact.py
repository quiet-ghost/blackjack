import customtkinter as ctk
import config
from game.blackjack import Blackjack
from game.player import Player
from gui.components import ModernCard, ModernButton, ModernChipDisplay, ModernBetSlider, ModernScoreDisplay
from gui.modern_stats import ModernStatsWindow
from gui.modal_dialogs import show_game_result, show_error, show_info

class ModernMainWindow:
    def __init__(self, auth):
        self.auth = auth
        self.user_data = auth.get_user_data()
        
        self.root = ctk.CTk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.minsize(800, 550)  # Smaller minimum size
        
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
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=config.COLORS['primary'])
        main_container.pack(fill="both", expand=True)
        
        # Create scrollable frame for better responsiveness
        self.scrollable_frame = ctk.CTkScrollableFrame(main_container, 
                                                      corner_radius=0,
                                                      fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_header()
        self.create_game_table()
        self.create_controls()
        self.update_display()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self.scrollable_frame, 
                                  height=80, 
                                  corner_radius=10, 
                                  fg_color=config.COLORS['secondary'])
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Left side - Game title
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=15)
        
        title_label = ctk.CTkLabel(left_frame, 
                                 text="🃏 BLACKJACK",
                                 font=('Segoe UI', 20, 'bold'),
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(anchor="w", pady=(10, 0))
        
        subtitle_label = ctk.CTkLabel(left_frame,
                                    text="Casino Experience",
                                    font=config.FONTS['small'],
                                    text_color=config.COLORS['text_secondary'])
        subtitle_label.pack(anchor="w")
        
        # Right side - User info
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=15)
        
        user_label = ctk.CTkLabel(right_frame,
                                text=f"👤 {self.auth.current_user}",
                                font=config.FONTS['body'],
                                text_color=config.COLORS['text_primary'])
        user_label.pack(anchor="e", pady=(8, 2))
        
        # Chip display and stats button
        user_controls = ctk.CTkFrame(right_frame, fg_color="transparent")
        user_controls.pack(anchor="e")
        
        self.chip_display = ModernChipDisplay(user_controls, self.player.chips)
        self.chip_display.pack(side="left", padx=(0, 8))
        
        stats_btn = ctk.CTkButton(user_controls, 
                                text="📊",
                                command=self.show_stats,
                                width=35,
                                height=35,
                                font=('Segoe UI', 14),
                                fg_color=config.COLORS['warning'],
                                hover_color=config.COLORS['warning'])
        stats_btn.pack(side="left")
        
    def create_game_table(self):
        # Game table with compact design
        table_frame = ctk.CTkFrame(self.scrollable_frame, 
                                 corner_radius=15, 
                                 fg_color=config.COLORS['table_green'])
        table_frame.pack(fill="x", pady=(0, 10))
        
        # Dealer section - more compact
        dealer_section = ctk.CTkFrame(table_frame, 
                                    corner_radius=10, 
                                    fg_color=config.COLORS['dealer_area'])
        dealer_section.pack(fill="x", padx=15, pady=(15, 8))
        
        dealer_header = ctk.CTkFrame(dealer_section, fg_color="transparent")
        dealer_header.pack(fill="x", pady=(10, 5))
        
        dealer_label = ctk.CTkLabel(dealer_header,
                                  text="🎩 DEALER",
                                  font=config.FONTS['body'],
                                  text_color=config.COLORS['text_primary'])
        dealer_label.pack(side="left", padx=15)
        
        # Compact score display
        self.dealer_score_label = ctk.CTkLabel(dealer_header,
                                             text="Score: 0",
                                             font=config.FONTS['body'],
                                             text_color=config.COLORS['text_secondary'])
        self.dealer_score_label.pack(side="right", padx=15)
        
        # Dealer cards area - more compact
        self.dealer_cards_frame = ctk.CTkFrame(dealer_section, fg_color="transparent")
        self.dealer_cards_frame.pack(pady=(5, 10))
        
        # Player section - more compact
        player_section = ctk.CTkFrame(table_frame, 
                                    corner_radius=10, 
                                    fg_color=config.COLORS['player_area'])
        player_section.pack(fill="x", padx=15, pady=(8, 15))
        
        player_header = ctk.CTkFrame(player_section, fg_color="transparent")
        player_header.pack(fill="x", pady=(10, 5))
        
        player_label = ctk.CTkLabel(player_header,
                                  text="🎮 PLAYER",
                                  font=config.FONTS['body'],
                                  text_color=config.COLORS['text_primary'])
        player_label.pack(side="left", padx=15)
        
        # Compact score display
        self.player_score_label = ctk.CTkLabel(player_header,
                                             text="Score: 0",
                                             font=config.FONTS['body'],
                                             text_color=config.COLORS['text_secondary'])
        self.player_score_label.pack(side="right", padx=15)
        
        # Player cards area - more compact
        self.player_cards_frame = ctk.CTkFrame(player_section, fg_color="transparent")
        self.player_cards_frame.pack(pady=(5, 10))
        
    def create_controls(self):
        # More compact controls
        controls_frame = ctk.CTkFrame(self.scrollable_frame, 
                                    height=120, 
                                    corner_radius=10, 
                                    fg_color=config.COLORS['secondary'])
        controls_frame.pack(fill="x")
        controls_frame.pack_propagate(False)
        
        # Left side - Betting controls (more compact)
        bet_section = ctk.CTkFrame(controls_frame, fg_color="transparent")
        bet_section.pack(side="left", fill="y", padx=15, pady=15)
        
        # Compact bet slider
        bet_label = ctk.CTkLabel(bet_section,
                               text="💰 Bet",
                               font=config.FONTS['small'],
                               text_color=config.COLORS['text_primary'])
        bet_label.pack()
        
        self.bet_var = ctk.IntVar(value=10)
        self.bet_slider = ctk.CTkSlider(bet_section,
                                      from_=1,
                                      to=min(self.player.chips, 100),
                                      variable=self.bet_var,
                                      width=150,
                                      height=16)
        self.bet_slider.pack(pady=5)
        
        self.bet_amount_label = ctk.CTkLabel(bet_section,
                                           text=f"${self.bet_var.get()}",
                                           font=config.FONTS['body'],
                                           text_color=config.COLORS['chips_gold'])
        self.bet_amount_label.pack()
        
        # Update bet display when slider changes
        self.bet_slider.configure(command=self.update_bet_display)
        
        # Right side - Game action buttons (more compact)
        buttons_section = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_section.pack(side="right", fill="y", padx=15, pady=15)
        
        # Single row of buttons
        button_row = ctk.CTkFrame(buttons_section, fg_color="transparent")
        button_row.pack()
        
        self.deal_btn = ctk.CTkButton(button_row, 
                                    text="🎴 Deal",
                                    command=self.deal_cards,
                                    width=80,
                                    height=35,
                                    font=config.FONTS['small'],
                                    fg_color=config.COLORS['accent'],
                                    hover_color=config.COLORS['accent_hover'])
        self.deal_btn.pack(side="left", padx=2)
        
        self.hit_btn = ctk.CTkButton(button_row, 
                                   text="👆 Hit",
                                   command=self.hit,
                                   width=80,
                                   height=35,
                                   font=config.FONTS['small'],
                                   fg_color=config.COLORS['success'],
                                   hover_color=config.COLORS['success'],
                                   state="disabled")
        self.hit_btn.pack(side="left", padx=2)
        
        self.stand_btn = ctk.CTkButton(button_row, 
                                     text="✋ Stand",
                                     command=self.stand,
                                     width=80,
                                     height=35,
                                     font=config.FONTS['small'],
                                     fg_color=config.COLORS['warning'],
                                     hover_color=config.COLORS['warning'],
                                     state="disabled")
        self.stand_btn.pack(side="left", padx=2)
        
        self.double_btn = ctk.CTkButton(button_row, 
                                      text="⚡ Double",
                                      command=self.double_down,
                                      width=80,
                                      height=35,
                                      font=config.FONTS['small'],
                                      fg_color=config.COLORS['danger'],
                                      hover_color=config.COLORS['danger'],
                                      state="disabled")
        self.double_btn.pack(side="left", padx=2)
        
    def update_bet_display(self, value):
        self.bet_amount_label.configure(text=f"${int(value)}")
        
    def get_bet_amount(self):
        return int(self.bet_var.get())
        
    def deal_cards(self):
        bet_amount = self.get_bet_amount()
        if not self.player.place_bet(bet_amount):
            show_error(self.root, "Insufficient Chips", "You don't have enough chips for this bet!")
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
            show_error(self.root, "Insufficient Chips", "You don't have enough chips to double down!")
            
    def clear_cards(self):
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        self.dealer_cards = []
        self.player_cards = []
        
    def display_cards(self):
        self.clear_cards()
        
        # Dealer cards - smaller and more compact
        for i, card in enumerate(self.game.dealerHand):
            hidden = i == 1 and self.game.currentTurn == "Player" and not self.game.gameOver
            card_widget = ModernCard(self.dealer_cards_frame, card, hidden)
            card_widget.pack(side="left", padx=3, pady=5)
            self.dealer_cards.append(card_widget)
            
        # Player cards - smaller and more compact
        for card in self.game.playerHand:
            card_widget = ModernCard(self.player_cards_frame, card)
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
            
        # Show custom modal instead of OS popup
        show_game_result(self.root, self.game.result, self.game.blackjack)
        
        self.save_game_stats()
        self.update_display()
        
        # Check if player is out of chips
        if self.player.chips <= 0:
            show_info(self.root, "Game Over", "You're out of chips! Thanks for playing!")
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
            
        self.auth.update_user_data(user_data)
        self.user_data.update(user_data)
        
    def show_stats(self):
        stats_window = ModernStatsWindow(self.root, self.user_data)
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        self.save_game_stats()
        self.root.destroy()

if __name__ == "__main__":
    from utils.auth import UserAuth
    auth = UserAuth()
    auth.current_user = "test"
    game = ModernMainWindow(auth)
    game.run()