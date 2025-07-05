import customtkinter as ctk
from tkinter import messagebox
import config
from game.blackjack import Blackjack
from game.player import Player
from gui.components import ModernCard, ModernButton, ModernChipDisplay, ModernBetSlider, ModernScoreDisplay
from gui.modern_stats import ModernStatsWindow

class ModernMainWindow:
    def __init__(self, auth):
        self.auth = auth
        self.user_data = auth.get_user_data()
        
        self.root = ctk.CTk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
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
        # Main container with gradient-like background
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=config.COLORS['primary'])
        main_container.pack(fill="both", expand=True)
        
        self.create_header(main_container)
        self.create_game_table(main_container)
        self.create_controls(main_container)
        self.update_display()
        
    def create_header(self, parent):
        header_frame = ctk.CTkFrame(parent, height=100, corner_radius=0, fg_color=config.COLORS['secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Left side - Game title
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20)
        
        title_label = ctk.CTkLabel(left_frame, 
                                 text="🃏 BLACKJACK",
                                 font=config.FONTS['title'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(anchor="w", pady=(15, 5))
        
        subtitle_label = ctk.CTkLabel(left_frame,
                                    text="Professional Casino Experience",
                                    font=config.FONTS['small'],
                                    text_color=config.COLORS['text_secondary'])
        subtitle_label.pack(anchor="w")
        
        # Right side - User info
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20)
        
        user_label = ctk.CTkLabel(right_frame,
                                text=f"👤 {self.auth.current_user}",
                                font=config.FONTS['subtitle'],
                                text_color=config.COLORS['text_primary'])
        user_label.pack(anchor="e", pady=(10, 5))
        
        # Chip display and stats button
        user_controls = ctk.CTkFrame(right_frame, fg_color="transparent")
        user_controls.pack(anchor="e")
        
        self.chip_display = ModernChipDisplay(user_controls, self.player.chips)
        self.chip_display.pack(side="left", padx=(0, 10))
        
        stats_btn = ModernButton(user_controls, "📊 Stats", self.show_stats, style="warning")
        stats_btn.pack(side="left")
        
    def create_game_table(self, parent):
        # Game table with felt-like appearance
        table_frame = ctk.CTkFrame(parent, corner_radius=20, fg_color=config.COLORS['table_green'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Dealer section
        dealer_section = ctk.CTkFrame(table_frame, corner_radius=15, fg_color=config.COLORS['dealer_area'])
        dealer_section.pack(fill="x", padx=30, pady=(30, 15))
        
        dealer_header = ctk.CTkFrame(dealer_section, fg_color="transparent")
        dealer_header.pack(fill="x", pady=(20, 10))
        
        dealer_label = ctk.CTkLabel(dealer_header,
                                  text="🎩 DEALER",
                                  font=config.FONTS['subtitle'],
                                  text_color=config.COLORS['text_primary'])
        dealer_label.pack(side="left", padx=20)
        
        self.dealer_score = ModernScoreDisplay(dealer_header, "Score", 0)
        self.dealer_score.pack(side="right", padx=20)
        
        # Dealer cards area
        self.dealer_cards_frame = ctk.CTkFrame(dealer_section, fg_color="transparent")
        self.dealer_cards_frame.pack(pady=(10, 20))
        
        # Player section
        player_section = ctk.CTkFrame(table_frame, corner_radius=15, fg_color=config.COLORS['player_area'])
        player_section.pack(fill="x", padx=30, pady=(15, 30))
        
        player_header = ctk.CTkFrame(player_section, fg_color="transparent")
        player_header.pack(fill="x", pady=(20, 10))
        
        player_label = ctk.CTkLabel(player_header,
                                  text="🎮 PLAYER",
                                  font=config.FONTS['subtitle'],
                                  text_color=config.COLORS['text_primary'])
        player_label.pack(side="left", padx=20)
        
        self.player_score = ModernScoreDisplay(player_header, "Score", 0)
        self.player_score.pack(side="right", padx=20)
        
        # Player cards area
        self.player_cards_frame = ctk.CTkFrame(player_section, fg_color="transparent")
        self.player_cards_frame.pack(pady=(10, 20))
        
    def create_controls(self, parent):
        controls_frame = ctk.CTkFrame(parent, height=150, corner_radius=15, fg_color=config.COLORS['secondary'])
        controls_frame.pack(fill="x", padx=20, pady=(10, 20))
        controls_frame.pack_propagate(False)
        
        # Left side - Betting controls
        bet_section = ctk.CTkFrame(controls_frame, fg_color="transparent")
        bet_section.pack(side="left", fill="y", padx=20, pady=20)
        
        self.bet_slider = ModernBetSlider(bet_section, min(self.player.chips, 100))
        self.bet_slider.pack()
        
        self.current_bet_label = ctk.CTkLabel(bet_section,
                                            text="Current Bet: $0",
                                            font=config.FONTS['body'],
                                            text_color=config.COLORS['text_secondary'])
        self.current_bet_label.pack(pady=(10, 0))
        
        # Right side - Game action buttons
        buttons_section = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_section.pack(side="right", fill="y", padx=20, pady=20)
        
        # Top row buttons
        top_buttons = ctk.CTkFrame(buttons_section, fg_color="transparent")
        top_buttons.pack(pady=(0, 10))
        
        self.deal_btn = ModernButton(top_buttons, "🎴 Deal Cards", self.deal_cards, style="primary")
        self.deal_btn.pack(side="left", padx=(0, 10))
        
        self.hit_btn = ModernButton(top_buttons, "👆 Hit", self.hit, enabled=False, style="success")
        self.hit_btn.pack(side="left", padx=(0, 10))
        
        # Bottom row buttons
        bottom_buttons = ctk.CTkFrame(buttons_section, fg_color="transparent")
        bottom_buttons.pack()
        
        self.stand_btn = ModernButton(bottom_buttons, "✋ Stand", self.stand, enabled=False, style="warning")
        self.stand_btn.pack(side="left", padx=(0, 10))
        
        self.double_btn = ModernButton(bottom_buttons, "⚡ Double", self.double_down, enabled=False, style="danger")
        self.double_btn.pack(side="left")
        
    def deal_cards(self):
        bet_amount = self.bet_slider.get_bet()
        if not self.player.place_bet(bet_amount):
            messagebox.showerror("Insufficient Chips", "You don't have enough chips for this bet!")
            return
            
        self.game_in_progress = True
        self.game.start_game()
        
        self.clear_cards()
        self.display_cards()
        self.update_display()
        
        if self.game.blackjack:
            self.root.after(1000, self.end_game)  # Delay to show cards
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
            messagebox.showerror("Insufficient Chips", "You don't have enough chips to double down!")
            
    def clear_cards(self):
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        self.dealer_cards = []
        self.player_cards = []
        
    def display_cards(self):
        self.clear_cards()
        
        # Dealer cards
        for i, card in enumerate(self.game.dealerHand):
            hidden = i == 1 and self.game.currentTurn == "Player" and not self.game.gameOver
            card_widget = ModernCard(self.dealer_cards_frame, card, hidden)
            card_widget.pack(side="left", padx=8, pady=10)
            self.dealer_cards.append(card_widget)
            
        # Player cards
        for card in self.game.playerHand:
            card_widget = ModernCard(self.player_cards_frame, card)
            card_widget.pack(side="left", padx=8, pady=10)
            self.player_cards.append(card_widget)
            
    def update_display(self):
        # Update scores
        if self.game.currentTurn == "Player" and not self.game.gameOver:
            dealer_visible = self.game.dealerHand[0].get_value() if self.game.dealerHand else 0
            self.dealer_score.update_score(dealer_visible, hidden=True)
        else:
            self.dealer_score.update_score(self.game.dealerScore)
            
        self.player_score.update_score(self.game.playerScore)
        
        # Update chip display
        self.chip_display.update_chips(self.player.chips)
        self.current_bet_label.configure(text=f"Current Bet: ${self.player.current_bet}")
        
        # Update bet slider
        max_bet = min(self.player.chips, 100) if not self.game_in_progress else 0
        self.bet_slider.set_max_bet(max_bet)
        
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
        
        # Determine result and show appropriate message
        result_messages = {
            "win": ("🎉 YOU WIN! 🎉", "Congratulations! You beat the dealer!"),
            "lose": ("😔 DEALER WINS", "Better luck next time!"),
            "draw": ("🤝 PUSH (TIE)", "It's a tie! Your bet is returned.")
        }
        
        if self.game.blackjack and self.game.result == "win":
            title, message = "🃏 BLACKJACK! 🃏", "Natural 21! You win 3:2!"
        else:
            title, message = result_messages.get(self.game.result, ("Game Over", ""))\n        
        # Handle winnings
        if self.game.result == "win":
            multiplier = 0.5 if self.game.blackjack else 1
            self.player.win_bet(multiplier)
        elif self.game.result == "lose":
            self.player.lose_bet()
        else:
            self.player.draw_bet()
            
        # Show result dialog
        messagebox.showinfo(title, message)
        
        self.save_game_stats()
        self.update_display()
        
        # Check if player is out of chips
        if self.player.chips <= 0:
            messagebox.showinfo("Game Over", "You're out of chips! Thanks for playing!")
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