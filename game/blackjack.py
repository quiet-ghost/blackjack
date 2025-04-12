# Core game logic (rules, deck, hands, etc.)
import random


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


class Blackjack:
    DECK_THRESHOLD = int(416 * 0.6)  # ~40% of the deck remaining

    def __init__(self):
        self.deck = []
        # TODO: Create player and dealer objects
        #        self.player = Player()
        #        self.dealer = Dealer()
        self.dealerScore = 0
        self.playerScore = 0
        self.gameOver = False
        self.currentTurn = "Player"
        self.playerBet = 0
        self.blackjack = False
        self.result = None
        self.playerHand = []
        self.dealerHand = []

    def create_deck(self):
        self.deck = []
        for suit in ["C", "D", "H", "S"] * 8:
            for rank in [
                "A",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
            ]:
                self.deck.append(Card(rank, suit))

    def shuffle_deck(self):
        if self.deck == []:
            self.create_deck()
            random.shuffle(self.deck)
        else:
            random.shuffle(self.deck)

    def check_deck(self):
        """Ensure deck has enough cards; refresh and shuffle if ≤ DECK_THRESHOLD or empty."""
        if not self.deck or len(self.deck) <= self.DECK_THRESHOLD:
            self.create_deck()
            self.shuffle_deck()

    def calculate_score(self, hand):
        total = 0
        aces = 0

        for card in hand:
            total += card.get_value()
            if card.isAce:
                aces += 1

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def deal_cards(self):
        self.check_deck()
        self.playerHand = []
        self.dealerHand = []
        self.playerScore = 0
        self.dealerScore = 0
        for i in range(2):
            self.playerHand.append(self.deck.pop())
            self.dealerHand.append(self.deck.pop())
        self.playerScore = self.calculate_score(self.playerHand)
        self.dealerScore = self.calculate_score(self.dealerHand)
        # self.check_blackjack() TODO: Implement check_blackjack()

    def place_bet(self):
        pass

    def hit(self):
        pass

    def stand(self):
        pass

    def split(self):
        pass

    def check_bust(self):
        pass

    def double_down(self):
        pass

    def dealer_turn(self):
        pass

    def determine_winner(self):
        pass

    def check_blackjack(self):
        pass

    def start_game(self):
        pass

    def reset_game(self):
        pass
