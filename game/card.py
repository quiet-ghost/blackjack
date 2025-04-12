class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.isAce = self.rank == "A"
        self.isJack = self.rank == "J"
        self.isQueen = self.rank == "Q"
        self.isKing = self.rank == "K"

    def get_value(self):
        # Logic to return value: 11 for Ace and 10 for Jack, Queen, and King, int(rank) for 2-10
        if self.isAce:
            return 11  # Ace is worth 11 or 1 will be done in calculate_score():
        elif self.isJack:
            return 10
        elif self.isQueen:
            return 10
        elif self.isKing:
            return 10
        else:
            return int(self.rank)

    def __str__(self):
        return self.rank + self.suit
