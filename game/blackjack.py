# Core game logic (rules, deck, hands, etc.)
import random
import pathlib
import time
from warnings import warn


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
    DECK_THRESHOLD = int(52 * 0.6)  # ~40% of the deck remaining

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
        for suit in ["C", "D", "H", "S"]:
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


if __name__ == "__main__":
    game = Blackjack()

    # Test create_deck()
    game.create_deck()
    print("After createDeck:")
    print("Deck length:", len(game.deck))
    print("First 5 cards:", [str(card) for card in game.deck[:5]])
    print("Last 5 cards:", [str(card) for card in game.deck[-5:]])
    print(" ")
    # Test shuffle_deck()
    game.shuffle_deck()
    print("\nAfter shuffleDeck:")
    print("Deck length:", len(game.deck))
    print("First 5 cards:", [str(card) for card in game.deck[:5]])
    print(" ")
    # Test shuffle_deck()
    # Test calculate_score()
    hand1 = [Card("A", "S"), Card("6", "H")]
    hand2 = [Card("A", "S"), Card("8", "H"), Card("7", "C")]
    hand3 = [Card("A", "S"), Card("A", "H")]
    hand4 = [Card("A", "S"), Card("K", "D")]
    print("Hand 1:", game.calculate_score(hand1))  # Expect 17
    print("Hand 2:", game.calculate_score(hand2))  # Expect 16
    print("Hand 3:", game.calculate_score(hand3))  # Expect 12
    print("Hand 4:", game.calculate_score(hand4))  # Expect 21
    print(" ")
    # Test deal_cards()
    game.deal_cards()
    print("\nAfter deal_cards:")
    print(
        "Player hand:",
        [str(card) for card in game.playerHand],
        "Score:",
        game.playerScore,
    )
    print(
        "Dealer hand:",
        [str(card) for card in game.dealerHand],
        "Score:",
        game.dealerScore,
    )
    print("Player hand length:", len(game.playerHand))
    print("Dealer hand length:", len(game.dealerHand))
    print("Deck length:", len(game.deck))
    print("Player score check:", game.calculate_score(game.playerHand))
    print("Dealer score check:", game.calculate_score(game.dealerHand))
    print(" ")
    # Test check_deck()
    game.deck = [Card("A", "S")] * 31  # Simulate low deck
    game.deal_cards()
    print("Deck length after low deck deal:", len(game.deck))  # Expect 48 (new deck)
