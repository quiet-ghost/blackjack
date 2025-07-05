class Dealer:
    def __init__(self):
        self.hand = []
        self.score = 0
        self.hidden_card = True
        
    def should_hit(self):
        return self.score < 17
        
    def reveal_card(self):
        self.hidden_card = False
        
    def reset_hand(self):
        self.hand = []
        self.score = 0
        self.hidden_card = True
