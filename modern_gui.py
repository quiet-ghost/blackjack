#!/usr/bin/env python3
"""
Modern Blackjack Casino - Launch Script
A sleek, professional blackjack game with modern UI
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the modern GUI version of the blackjack game"""
    try:
        print("🎮 Starting Modern Blackjack Casino...")
        print("🃏 Welcome to Modern Blackjack Casino!")
        print("✨ Loading modern interface...")
        
        # Test imports first
        try:
            import customtkinter as ctk
            import tkinter as tk
            print("✅ CustomTkinter available")
        except ImportError as e:
            print(f"❌ CustomTkinter not available: {e}")
            raise
            
        from gui.modern_login import ModernLoginWindow
        
        app = ModernLoginWindow()
        app.run()
        
    except ImportError as e:
        print("❌ Error: Missing required dependencies")
        print("Please install required packages:")
        print("  pip install customtkinter pillow")
        print(f"Details: {e}")
        
        # Fallback to old GUI
        print("\n🔄 Falling back to classic interface...")
        try:
            from gui.login_window import LoginWindow
            app = LoginWindow()
            app.run()
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            print("Please check your Python installation and dependencies.")
        
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
        
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback to old GUI
        print("\n🔄 Falling back to classic interface...")
        try:
            from gui.login_window import LoginWindow
            app = LoginWindow()
            app.run()
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            print("Please check your Python installation and dependencies.")

if __name__ == "__main__":
    main()