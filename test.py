from game.blackjack import Blackjack, Card

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
