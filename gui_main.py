#!/usr/bin/env python3

from gui.login_window import LoginWindow

def main():
    """Launch the GUI version of the blackjack game"""
    try:
        app = LoginWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()