from game.blackjack import Blackjack
from game.card import Card

game = Blackjack()

# Test create_deck()
game.create_deck()
print("After createDeck:")
print("Deck length:", len(game.deck))
print("First 5 cards:", [str(card) for card in game.deck[:5]])
print("Last 5 cards:", [str(card) for card in game.deck[-5:]])

# Test shuffle_deck()
game.shuffle_deck()
print("\nAfter shuffleDeck:")
print("Deck length:", len(game.deck))
print("First 5 cards:", [str(card) for card in game.deck[:5]])

print(" ")

# Test shuffle_deck()
hand1 = [Card("A", "S"), Card("6", "H")]
hand2 = [Card("A", "S"), Card("8", "H"), Card("7", "C")]
hand3 = [Card("A", "S"), Card("A", "H")]
hand4 = [Card("A", "S"), Card("K", "D")]

print("testing calculate_score()")
# Test calculate_score()
print("Hand 1:", game.calculate_score(hand1))  # Expect 17
print("Hand 2:", game.calculate_score(hand2))  # Expect 16
print("Hand 3:", game.calculate_score(hand3))  # Expect 12
print("Hand 4:", game.calculate_score(hand4))  # Expect 21

print(" ")

print("testing deal_cards:")
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
print("testing check_deck()")
# Test check_deck()
game.deck = [Card("A", "S")] * 31  # Simulate low deck
game.deal_cards()
print("Deck length after low deck deal:", len(game.deck))  # Expect 48 (new deck)

print(" ")

# Test check_blackjack()
print("Blackjack:", game.blackjack)  # Expect False
game.playerHand = [Card("A", "S"), Card("K", "D")]
game.dealerHand = [Card("A", "S"), Card("K", "D")]
game.blackjack = False
game.check_blackjack()
print("Blackjack:", game.blackjack)  # Expect True

print(" ")

game.playerBet = 10
game.deal_cards()
print("\nAfter deal_cards:")
print(
    "Player hand:", [str(card) for card in game.playerHand], "Score:", game.playerScore
)
print(
    "Dealer hand:", [str(card) for card in game.dealerHand], "Score:", game.dealerScore
)
print("Blackjack:", game.blackjack, "Result:", game.result, "Game Over:", game.gameOver)
print("Blackjack Payout:", game.playerBlackjackPayout)
print("Winnings:", game.determine_winner())

# Test 1: Player Blackjack
game = Blackjack()
game.playerBet = 10
game.playerHand = [Card("A", "S"), Card("K", "D")]  # 21
game.dealerHand = [Card("6", "H"), Card("7", "C")]  # 13
game.playerScore = game.calculate_score(game.playerHand)
game.dealerScore = game.calculate_score(game.dealerHand)
game.check_blackjack()
print(
    "\nPlayer BJ:",
    game.blackjack,
    game.result,
    game.gameOver,
    game.playerBlackjackPayout,
    game.determine_winner(),
)
# True, "win", True, True, 15

# Test 2: 10 + Queen (No Blackjack)
game = Blackjack()
game.playerBet = 10
game.playerHand = [Card("10", "H"), Card("Q", "C")]  # 20
game.dealerHand = [Card("8", "S"), Card("9", "D")]  # 17
game.playerScore = game.calculate_score(game.playerHand)
game.dealerScore = game.calculate_score(game.dealerHand)
game.check_blackjack()
print(
    "10+Q:",
    game.blackjack,
    game.result,
    game.gameOver,
    game.playerBlackjackPayout,
    game.determine_winner(),
)  # False, None, False, False, 0
# Expected Output
