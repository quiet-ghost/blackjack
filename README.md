# 🃏 Modern Blackjack Casino

A professional-grade blackjack game with both classic and modern user interfaces, featuring persistent user accounts, statistics tracking, and achievement systems.

## ✨ Features

### 🎮 Game Features
- **Complete Blackjack Rules**: Hit, Stand, Double Down, proper dealer logic
- **8-Deck Shoe**: Professional casino-style card dealing
- **Blackjack Detection**: Automatic natural 21 detection with 3:2 payout
- **Smart Dealer**: Dealer hits on soft 17, stands on 17+

### 👤 User System
- **User Registration & Login**: Secure account system
- **Persistent Data**: Chips and statistics saved between sessions
- **Multiple Players**: Each user has their own profile and progress

### 📊 Statistics & Achievements
- **Detailed Stats**: Games played, won, lost, win rate tracking
- **Achievement System**: Unlock achievements based on performance
- **Performance Rating**: From Beginner to Legendary based on win rate
- **Profit/Loss Tracking**: Monitor your casino performance

### 🎨 Dual Interface Options

#### Classic Interface (Tkinter)
- Traditional desktop application look
- Compatible with all Python installations
- Lightweight and fast

#### Modern Interface (CustomTkinter)
- **Sleek Dark Theme**: Professional casino aesthetic
- **Rounded Corners**: Modern card and button designs
- **Color-Coded Elements**: Intuitive visual feedback
- **Animated Cards**: Smooth card dealing animations
- **Responsive Layout**: Optimized spacing and typography

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python 3.8+ and tkinter
sudo apt-get install python3 python3-tk python3-pip

# Or on macOS
brew install python-tk

# Or on Windows - tkinter comes with Python
```

### Installation

1. **Clone or download the project**
2. **Set up virtual environment (recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install modern UI dependencies** (optional):
   ```bash
   pip install customtkinter pillow
   ```

### Running the Game

#### Modern Interface (Recommended)
```bash
python modern_gui.py
```

#### Classic Interface
```bash
python gui_main.py
```

#### Console Version
```bash
python main.py
```

## 🎯 How to Play

1. **Register/Login**: Create an account or login with existing credentials
2. **Place Bet**: Use the slider to set your bet amount
3. **Deal Cards**: Click "Deal Cards" to start a new hand
4. **Make Decisions**: 
   - **Hit**: Take another card
   - **Stand**: Keep your current hand
   - **Double**: Double your bet and take exactly one more card
5. **Win Conditions**:
   - Get 21 with your first two cards (Blackjack) - pays 3:2
   - Get closer to 21 than the dealer without going over
   - Dealer busts (goes over 21)

## 📁 Project Structure

```
blackjack/
├── game/                   # Core game logic
│   ├── blackjack.py      # Main game class
│   ├── card.py           # Card representation
│   ├── player.py         # Player class
│   └── dealer.py         # Dealer class
├── gui/                   # User interface
│   ├── components.py     # Reusable UI components
│   ├── login_window.py   # Classic login interface
│   ├── main_window.py    # Classic game interface
│   ├── stats_window.py   # Classic stats interface
│   ├── modern_login.py   # Modern login interface
│   ├── modern_main.py    # Modern game interface
│   └── modern_stats.py   # Modern stats interface
├── utils/                 # Utilities
│   └── auth.py           # User authentication
├── database/             # Data storage
│   └── users.json        # User data (auto-created)
├── config.py             # Game configuration
├── main.py              # Console version launcher
├── gui_main.py          # Classic GUI launcher
└── modern_gui.py        # Modern GUI launcher
```

## 🎨 Modern UI Highlights

### Login Screen
- **Casino Branding**: Professional title with card emojis
- **Feature Showcase**: Highlights game capabilities
- **Smooth Forms**: Modern input fields with placeholders
- **Dual Actions**: Login and Register in one interface

### Game Table
- **Casino Green Felt**: Authentic table appearance
- **Separated Areas**: Distinct dealer and player zones
- **Live Score Display**: Real-time score updates with color coding
- **Professional Cards**: Suit symbols with proper red/black coloring

### Control Panel
- **Interactive Betting**: Smooth slider with live preview
- **Action Buttons**: Color-coded game actions (Hit=Green, Stand=Yellow, etc.)
- **Chip Counter**: Live chip balance with coin emoji
- **Smart Enabling**: Buttons enable/disable based on game state

### Statistics Dashboard
- **Performance Grid**: Card-based stat display
- **Achievement Gallery**: Visual achievement showcase
- **Performance Rating**: Skill level assessment
- **Profit Analysis**: Financial performance tracking

## 🏆 Achievement System

Unlock achievements by playing:

- 🎮 **First Game**: Play your first hand
- 🔥 **Veteran Player**: Play 10+ games
- ⭐ **Blackjack Master**: Play 50+ games
- 💎 **Century Club**: Play 100+ games
- 🏆 **Winner**: Win 5+ games
- 👑 **Champion**: Win 20+ games
- 💰 **High Roller**: Reach $2,000 in chips
- 🎯 **Sharp Player**: Maintain 60%+ win rate
- 🧠 **Card Counter**: Maintain 75%+ win rate

## 🔧 Configuration

Edit `config.py` to customize:
- Window dimensions
- Color schemes
- Font settings
- Card and button sizes
- Starting chip amounts
- Animation timings

## 🐛 Troubleshooting

### "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# macOS
brew install python-tk
```

### "No module named 'customtkinter'"
```bash
pip install customtkinter pillow
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install customtkinter pillow
```

## 🎲 Game Rules Reference

- **Blackjack**: 21 with first two cards (Ace + 10-value card)
- **Bust**: Hand total exceeds 21
- **Soft Hand**: Hand containing an Ace counted as 11
- **Hard Hand**: Hand with no Aces or Aces counted as 1
- **Dealer Rules**: Hits on 16 and soft 17, stands on hard 17+
- **Payouts**: Blackjack pays 3:2, regular wins pay 1:1

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the game!

---

**Enjoy playing Modern Blackjack Casino! 🎰**