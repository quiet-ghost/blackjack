# Core game logic (rules, deck, hands, etc.)
import random

from game.card import Card


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
        self.playerBlackjackPayout = False
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
        self.check_blackjack()

    def check_blackjack(self):
        player_blackjack = (
            len(self.playerHand) == 2
            and self.calculate_score(self.playerHand) == 21
            and any(card.isAce for card in self.playerHand)
        )
        dealer_blackjack = (
            len(self.dealerHand) == 2
            and self.calculate_score(self.dealerHand) == 21
            and any(card.isAce for card in self.dealerHand)
        )
        if player_blackjack and dealer_blackjack:
            self.blackjack = True
            self.result = "draw"
            self.gameOver = True
            self.playerBlackjackPayout = False
        elif player_blackjack:
            self.blackjack = True
            self.result = "win"
            self.gameOver = True
            self.playerBlackjackPayout = True
        elif dealer_blackjack:
            self.blackjack = True
            self.result = "lose"
            self.gameOver = True
            self.playerBlackjackPayout = False
        return self.blackjack

    def determine_winner(self):
        if self.playerScore > 21:
            self.result = "lose"
        elif self.dealerScore > 21:
            self.result = "win"
        elif self.playerScore > self.dealerScore:
            self.result = "win"
        elif self.playerScore < self.dealerScore:
            self.result = "lose"
        else:
            self.result = "draw"
        self.gameOver = True

    def place_bet(self):
        pass

    def hit(self):
        if not self.gameOver and self.currentTurn == "Player":
            self.check_deck()
            self.playerHand.append(self.deck.pop())
            self.playerScore = self.calculate_score(self.playerHand)
            if self.playerScore > 21:
                self.result = "lose"
                self.gameOver = True

    def stand(self):
        if not self.gameOver and self.currentTurn == "Player":
            self.currentTurn = "Dealer"
            self.dealer_turn()

    def split(self):
        pass

    def check_bust(self):
        return self.playerScore > 21 or self.dealerScore > 21

    def double_down(self):
        pass

    def dealer_turn(self):
        while self.dealerScore < 17:
            self.check_deck()
            self.dealerHand.append(self.deck.pop())
            self.dealerScore = self.calculate_score(self.dealerHand)
        self.determine_winner()

    def start_game(self):
        self.reset_game()
        self.deal_cards()

    def reset_game(self):
        self.dealerScore = 0
        self.playerScore = 0
        self.gameOver = False
        self.currentTurn = "Player"
        self.playerBet = 0
        self.blackjack = False
        self.playerBlackjackPayout = False
        self.result = None
        self.playerHand = []
        self.dealerHand = []
