import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import config


class ModernCard(ctk.CTkFrame):
    def __init__(self, parent, card=None, hidden=False):
        super().__init__(
            parent,
            width=config.CARD_WIDTH,
            height=config.CARD_HEIGHT,
            corner_radius=config.CARD_CORNER_RADIUS,
            fg_color=config.COLORS["card_bg"],
            border_width=2,
            border_color=config.COLORS["text_muted"],
        )

        self.card = card
        self.hidden = hidden
        self.create_card()

    def create_card(self):
        if self.hidden:
            # Card back design
            back_label = ctk.CTkLabel(
                self,
                text="🂠",
                font=config.FONTS["card"],
                text_color=config.COLORS["accent"],
            )
            back_label.place(relx=0.5, rely=0.5, anchor="center")

        elif self.card:
            # Card front with suit and rank
            suit_color = "#dc2626" if self.card.suit in ["H", "D"] else "#1f2937"
            suit_symbols = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}

            # Rank in top-left
            rank_label = ctk.CTkLabel(
                self,
                text=self.card.rank,
                font=("Segoe UI", 16, "bold"),
                text_color=suit_color,
            )
            rank_label.place(x=8, y=8)

            # Large suit symbol in center
            suit_label = ctk.CTkLabel(
                self,
                text=suit_symbols[self.card.suit],
                font=("Segoe UI", 40, "bold"),
                text_color=suit_color,
            )
            suit_label.place(relx=0.5, rely=0.5, anchor="center")

            # Small rank in bottom-right (rotated)
            small_rank = ctk.CTkLabel(
                self,
                text=self.card.rank,
                font=("Segoe UI", 12, "bold"),
                text_color=suit_color,
            )
            small_rank.place(x=config.CARD_WIDTH - 20, y=config.CARD_HEIGHT - 25)


class ModernButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, enabled=True, style="primary"):
        colors = {
            "primary": (config.COLORS["accent"], config.COLORS["accent_hover"]),
            "success": (config.COLORS["success"], config.COLORS["accent_hover"]),
            "warning": (config.COLORS["warning"], config.COLORS["warning"]),
            "danger": (config.COLORS["danger"], config.COLORS["danger"]),
        }

        fg_color, hover_color = colors.get(style, colors["primary"])

        super().__init__(
            parent,
            text=text,
            command=command,
            width=config.BUTTON_WIDTH,
            height=config.BUTTON_HEIGHT,
            corner_radius=config.BUTTON_CORNER_RADIUS,
            font=config.FONTS["button"],
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=config.COLORS["text_primary"],
        )

        if not enabled:
            self.configure(state="disabled")


class ModernChipDisplay(ctk.CTkFrame):
    def __init__(self, parent, chips=0):
        super().__init__(parent, corner_radius=10, fg_color=config.COLORS["secondary"])
        self.chips = chips
        self.create_display()

    def create_display(self):
        # Chip icon
        chip_label = ctk.CTkLabel(
            self,
            text="🪙",
            font=("Segoe UI", 24),
            text_color=config.COLORS["chips_gold"],
        )
        chip_label.pack(side="left", padx=(10, 5), pady=10)

        # Amount
        self.amount_label = ctk.CTkLabel(
            self,
            text=f"${self.chips:,}",
            font=config.FONTS["subtitle"],
            text_color=config.COLORS["text_primary"],
        )
        self.amount_label.pack(side="left", padx=(0, 10), pady=10)

    def update_chips(self, amount):
        self.chips = amount
        self.amount_label.configure(text=f"${self.chips:,}")


class ModernBetSlider(ctk.CTkFrame):
    def __init__(self, parent, max_bet=100, callback=None):
        super().__init__(parent, corner_radius=10, fg_color=config.COLORS["secondary"])
        self.max_bet = max_bet
        self.callback = callback
        self.create_slider()

    def create_slider(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="💰 Bet Amount",
            font=config.FONTS["body"],
            text_color=config.COLORS["text_primary"],
        )
        title_label.pack(pady=(15, 5))

        # Slider
        self.bet_var = tk.IntVar(value=10)
        self.slider = ctk.CTkSlider(
            self,
            from_=1,
            to=self.max_bet,
            variable=self.bet_var,
            command=self.on_change,
            width=200,
            height=20,
            button_color=config.COLORS["accent"],
            button_hover_color=config.COLORS["accent_hover"],
            progress_color=config.COLORS["accent"],
        )
        self.slider.pack(pady=10, padx=20)

        # Current bet display
        self.bet_label = ctk.CTkLabel(
            self,
            text=f"${self.bet_var.get()}",
            font=config.FONTS["subtitle"],
            text_color=config.COLORS["chips_gold"],
        )
        self.bet_label.pack(pady=(0, 15))

    def on_change(self, value):
        self.bet_label.configure(text=f"${int(value)}")
        if self.callback:
            self.callback(int(value))

    def get_bet(self):
        return int(self.bet_var.get())

    def set_max_bet(self, max_bet):
        self.max_bet = max_bet
        self.slider.configure(to=max_bet)
        if self.bet_var.get() > max_bet:
            self.bet_var.set(max_bet)


class ModernScoreDisplay(ctk.CTkFrame):
    def __init__(self, parent, title, score=0):
        super().__init__(
            parent,
            corner_radius=10,
            fg_color=config.COLORS["secondary"],
            border_width=2,
            border_color=config.COLORS["accent"],
        )

        self.title = title
        self.score = score
        self.create_display()

    def create_display(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=config.FONTS["subtitle"],
            text_color=config.COLORS["text_secondary"],
        )
        title_label.pack(pady=(10, 5))

        # Score
        self.score_label = ctk.CTkLabel(
            self,
            text=str(self.score),
            font=("Segoe UI", 32, "bold"),
            text_color=config.COLORS["text_primary"],
        )
        self.score_label.pack(pady=(0, 10))

    def update_score(self, score, hidden=False):
        self.score = score
        if hidden:
            self.score_label.configure(text="?")
        else:
            self.score_label.configure(text=str(score))

        # Color coding for score
        if score > 21:
            self.score_label.configure(text_color=config.COLORS["danger"])
        elif score == 21:
            self.score_label.configure(text_color=config.COLORS["success"])
        else:
            self.score_label.configure(text_color=config.COLORS["text_primary"])
