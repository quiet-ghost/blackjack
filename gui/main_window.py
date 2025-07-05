import tkinter as tk
from tkinter import messagebox
import config
from game.blackjack import Blackjack
from game.player import Player
from gui.components import CardWidget, GameButton, ChipDisplay, BetSlider
from gui.stats_window import StatsWindow

class MainWindow:
    def __init__(self, auth):
        self.auth = auth
        self.user_data = auth.get_user_data()
        
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.COLORS['background'])
        self.root.resizable(False, False)
        
        self.game = Blackjack()
        self.player = Player(self.auth.current_user, self.user_data['chips'])
        
        self.dealer_cards = []
        self.player_cards = []
        self.game_in_progress = False
        
        self.setup_ui()
        
    def setup_ui(self):
        self.create_header()
        self.create_game_area()
        self.create_controls()
        self.update_display()
        
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=config.COLORS['background'], height=80)
        header_frame.pack(fill='x', padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="BLACKJACK", 
                              font=config.FONTS['title'],
                              bg=config.COLORS['background'], 
                              fg=config.COLORS['text_primary'])
        title_label.pack(side='left')
        
        user_frame = tk.Frame(header_frame, bg=config.COLORS['background'])
        user_frame.pack(side='right')
        
        user_label = tk.Label(user_frame, text=f"Player: {self.auth.current_user}", 
                             font=config.FONTS['subtitle'],
                             bg=config.COLORS['background'], 
                             fg=config.COLORS['text_secondary'])
        user_label.pack()
        
        self.chip_display = ChipDisplay(user_frame, self.player.chips)
        self.chip_display.pack()
        
        stats_btn = tk.Button(user_frame, text="Stats", command=self.show_stats,
                             font=config.FONTS['body'], width=8,
                             bg=config.COLORS['button_bg'], fg=config.COLORS['button_text'])
        stats_btn.pack(pady=5)
        
    def create_game_area(self):
        game_frame = tk.Frame(self.root, bg=config.COLORS['background'])
        game_frame.pack(expand=True, fill='both', padx=20)
        
        dealer_frame = tk.Frame(game_frame, bg=config.COLORS['dealer_area'], height=200)
        dealer_frame.pack(fill='x', pady=10)
        dealer_frame.pack_propagate(False)
        
        dealer_label = tk.Label(dealer_frame, text="DEALER", 
                               font=config.FONTS['subtitle'],
                               bg=config.COLORS['dealer_area'], 
                               fg=config.COLORS['text_primary'])
        dealer_label.pack(pady=10)
        
        self.dealer_score_label = tk.Label(dealer_frame, text="Score: 0", 
                                          font=config.FONTS['body'],
                                          bg=config.COLORS['dealer_area'], 
                                          fg=config.COLORS['text_secondary'])
        self.dealer_score_label.pack()
        
        self.dealer_cards_frame = tk.Frame(dealer_frame, bg=config.COLORS['dealer_area'])
        self.dealer_cards_frame.pack(pady=10)
        
        player_frame = tk.Frame(game_frame, bg=config.COLORS['player_area'], height=200)
        player_frame.pack(fill='x', pady=10)
        player_frame.pack_propagate(False)
        
        player_label = tk.Label(player_frame, text="PLAYER", 
                               font=config.FONTS['subtitle'],
                               bg=config.COLORS['player_area'], 
                               fg=config.COLORS['text_primary'])
        player_label.pack(pady=10)
        
        self.player_score_label = tk.Label(player_frame, text="Score: 0", 
                                          font=config.FONTS['body'],
                                          bg=config.COLORS['player_area'], 
                                          fg=config.COLORS['text_secondary'])
        self.player_score_label.pack()
        
        self.player_cards_frame = tk.Frame(player_frame, bg=config.COLORS['player_area'])
        self.player_cards_frame.pack(pady=10)
        
    def create_controls(self):
        controls_frame = tk.Frame(self.root, bg=config.COLORS['background'], height=120)
        controls_frame.pack(fill='x', padx=20, pady=10)
        controls_frame.pack_propagate(False)
        
        bet_frame = tk.Frame(controls_frame, bg=config.COLORS['background'])
        bet_frame.pack(side='left', fill='y')
        
        self.bet_slider = BetSlider(bet_frame, min(self.player.chips, 100))
        self.bet_slider.pack(pady=10)
        
        self.current_bet_label = tk.Label(bet_frame, text="Current Bet: $0", 
                                         font=config.FONTS['body'],
                                         bg=config.COLORS['background'], 
                                         fg=config.COLORS['text_primary'])
        self.current_bet_label.pack()
        
        buttons_frame = tk.Frame(controls_frame, bg=config.COLORS['background'])
        buttons_frame.pack(side='right', fill='y')
        
        self.deal_btn = GameButton(buttons_frame, "Deal", self.deal_cards)
        self.deal_btn.pack(side='left', padx=5)
        
        self.hit_btn = GameButton(buttons_frame, "Hit", self.hit, enabled=False)
        self.hit_btn.pack(side='left', padx=5)
        
        self.stand_btn = GameButton(buttons_frame, "Stand", self.stand, enabled=False)
        self.stand_btn.pack(side='left', padx=5)
        
        self.double_btn = GameButton(buttons_frame, "Double", self.double_down, enabled=False)
        self.double_btn.pack(side='left', padx=5)
        
    def deal_cards(self):
        bet_amount = self.bet_slider.get_bet()
        if not self.player.place_bet(bet_amount):
            messagebox.showerror("Error", "Insufficient chips!")
            return
            
        self.game_in_progress = True
        self.game.start_game()
        
        self.clear_cards()
        self.display_cards()
        self.update_display()
        
        if self.game.blackjack:
            self.end_game()
        else:
            self.enable_game_buttons()
            
    def hit(self):
        self.game.hit()
        self.display_cards()
        self.update_display()
        
        if self.game.gameOver:
            self.end_game()
            
    def stand(self):
        self.game.stand()
        self.display_cards()
        self.update_display()
        self.end_game()
        
    def double_down(self):
        if self.player.chips >= self.player.current_bet:
            self.player.chips -= self.player.current_bet
            self.player.current_bet *= 2
            self.game.hit()
            if not self.game.gameOver:
                self.game.stand()
            self.display_cards()
            self.update_display()
            self.end_game()
        else:
            messagebox.showerror("Error", "Insufficient chips to double down!")
            
    def clear_cards(self):
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        self.dealer_cards = []
        self.player_cards = []
        
    def display_cards(self):
        self.clear_cards()
        
        for i, card in enumerate(self.game.dealerHand):
            hidden = i == 1 and self.game.currentTurn == "Player" and not self.game.gameOver
            card_widget = CardWidget(self.dealer_cards_frame, card, hidden)
            card_widget.pack(side='left', padx=5)
            self.dealer_cards.append(card_widget)
            
        for card in self.game.playerHand:
            card_widget = CardWidget(self.player_cards_frame, card)
            card_widget.pack(side='left', padx=5)
            self.player_cards.append(card_widget)
            
    def update_display(self):
        if self.game.currentTurn == "Player" and not self.game.gameOver:
            dealer_score = self.game.dealerHand[0].get_value() if self.game.dealerHand else 0
            self.dealer_score_label.configure(text=f"Score: {dealer_score}+")
        else:
            self.dealer_score_label.configure(text=f"Score: {self.game.dealerScore}")
            
        self.player_score_label.configure(text=f"Score: {self.game.playerScore}")
        self.chip_display.update_chips(self.player.chips)
        self.current_bet_label.configure(text=f"Current Bet: ${self.player.current_bet}")
        
        max_bet = min(self.player.chips, 100) if not self.game_in_progress else 0
        self.bet_slider.set_max_bet(max_bet)
        
    def enable_game_buttons(self):
        self.deal_btn.configure(state='disabled')
        self.hit_btn.configure(state='normal')
        self.stand_btn.configure(state='normal')
        
        can_double = (len(self.game.playerHand) == 2 and 
                     self.player.chips >= self.player.current_bet)
        self.double_btn.configure(state='normal' if can_double else 'disabled')
        
    def disable_game_buttons(self):
        self.deal_btn.configure(state='normal')
        self.hit_btn.configure(state='disabled')
        self.stand_btn.configure(state='disabled')
        self.double_btn.configure(state='disabled')
        
    def end_game(self):
        self.game_in_progress = False
        self.disable_game_buttons()
        
        result_text = ""
        if self.game.result == "win":
            multiplier = 0.5 if self.game.blackjack else 1
            self.player.win_bet(multiplier)
            result_text = "BLACKJACK! You Win!" if self.game.blackjack else "You Win!"
        elif self.game.result == "lose":
            self.player.lose_bet()
            result_text = "Dealer Wins!"
        else:
            self.player.draw_bet()
            result_text = "Push (Tie)!"
            
        messagebox.showinfo("Game Over", result_text)
        
        self.save_game_stats()
        self.update_display()
        
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
        stats_window = StatsWindow(self.root, self.user_data)
        
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
    game = MainWindow(auth)
    game.run()