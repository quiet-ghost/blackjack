class Player:
    def __init__(self, name="Player", chips=1000):
        self.name = name
        self.chips = chips
        self.current_bet = 0
        self.hands = []
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
    def place_bet(self, amount):
        if amount <= self.chips:
            self.current_bet = amount
            self.chips -= amount
            return True
        return False
    
    def win_bet(self, multiplier=1):
        winnings = self.current_bet * (1 + multiplier)
        self.chips += winnings
        self.wins += 1
        self.current_bet = 0
        
    def lose_bet(self):
        self.losses += 1
        self.current_bet = 0
        
    def draw_bet(self):
        self.chips += self.current_bet
        self.draws += 1
        self.current_bet = 0
        
    def get_stats(self):
        total_games = self.wins + self.losses + self.draws
        if total_games == 0:
            return {"games": 0, "win_rate": 0}
        return {
            "games": total_games,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "win_rate": round(self.wins / total_games * 100, 2)
        }
