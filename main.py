from game.blackjack import Blackjack
from game.player import Player
from game.dealer import Dealer

def main():
    print("Welcome to Blackjack!")
    game = Blackjack()
    player = Player("Player", 1000)
    
    while True:
        print(f"\nChips: {player.chips}")
        if player.chips <= 0:
            print("You're out of chips! Game over.")
            break
            
        try:
            bet = int(input("Enter your bet (0 to quit): "))
            if bet == 0:
                break
            if not player.place_bet(bet):
                print("Insufficient chips!")
                continue
        except ValueError:
            print("Invalid bet amount!")
            continue
            
        game.start_game()
        
        print(f"\nYour hand: {[str(card) for card in game.playerHand]} (Score: {game.playerScore})")
        print(f"Dealer's hand: [{str(game.dealerHand[0])}, Hidden] (Visible score: {game.dealerHand[0].get_value()})")
        
        if game.blackjack:
            print(f"Result: {game.result.upper()}")
            if game.result == "win":
                player.win_bet(0.5)  # Blackjack pays 3:2
            elif game.result == "lose":
                player.lose_bet()
            else:
                player.draw_bet()
            continue
            
        while not game.gameOver and game.currentTurn == "Player":
            action = input("Hit (h) or Stand (s)? ").lower()
            if action == 'h':
                game.hit()
                print(f"Your hand: {[str(card) for card in game.playerHand]} (Score: {game.playerScore})")
                if game.playerScore > 21:
                    print("Bust!")
            elif action == 's':
                game.stand()
            else:
                print("Invalid action!")
                
        if not game.blackjack:
            print(f"\nDealer's hand: {[str(card) for card in game.dealerHand]} (Score: {game.dealerScore})")
            print(f"Result: {game.result.upper()}")
            
        if game.result == "win":
            player.win_bet()
        elif game.result == "lose":
            player.lose_bet()
        else:
            player.draw_bet()
    
    stats = player.get_stats()
    print(f"\nFinal Stats: {stats['games']} games, {stats['wins']} wins, Win rate: {stats['win_rate']}%")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
