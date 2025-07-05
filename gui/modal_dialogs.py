import customtkinter as ctk
import config

class CustomModal:
    def __init__(self, parent, title, message, modal_type="info", buttons=None):
        self.parent = parent
        self.result = None
        self.modal_type = modal_type
        
        # Create overlay
        self.overlay = ctk.CTkFrame(parent, fg_color=("gray75", "gray25"))
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create modal window
        self.modal = ctk.CTkFrame(self.overlay, 
                                corner_radius=15,
                                fg_color=config.COLORS['secondary'],
                                border_width=2,
                                border_color=config.COLORS['accent'])
        
        # Center the modal
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        
        self.setup_modal(title, message, buttons)
        
        # Make modal grab focus
        self.overlay.grab_set()
        self.overlay.focus_set()
        
    def setup_modal(self, title, message, buttons):
        # Icon based on type
        icons = {
            "info": "ℹ️",
            "success": "✅", 
            "warning": "⚠️",
            "error": "❌",
            "question": "❓"
        }
        
        colors = {
            "info": config.COLORS['accent'],
            "success": config.COLORS['success'],
            "warning": config.COLORS['warning'], 
            "error": config.COLORS['danger'],
            "question": config.COLORS['accent']
        }
        
        icon = icons.get(self.modal_type, "ℹ️")
        color = colors.get(self.modal_type, config.COLORS['accent'])
        
        # Header with icon
        header_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        header_frame.pack(pady=(20, 10), padx=20)
        
        icon_label = ctk.CTkLabel(header_frame,
                                text=icon,
                                font=('Segoe UI', 32),
                                text_color=color)
        icon_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame,
                                 text=title,
                                 font=config.FONTS['subtitle'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack()
        
        # Message
        message_label = ctk.CTkLabel(self.modal,
                                   text=message,
                                   font=config.FONTS['body'],
                                   text_color=config.COLORS['text_secondary'],
                                   wraplength=300)
        message_label.pack(pady=(0, 20), padx=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20)
        
        if buttons is None:
            # Default OK button
            ok_btn = ctk.CTkButton(button_frame,
                                 text="OK",
                                 command=self.close_modal,
                                 width=100,
                                 height=35,
                                 font=config.FONTS['body'],
                                 fg_color=color,
                                 hover_color=color)
            ok_btn.pack()
        else:
            # Custom buttons
            for i, (text, command, style) in enumerate(buttons):
                btn_color = colors.get(style, config.COLORS['accent'])
                btn = ctk.CTkButton(button_frame,
                                  text=text,
                                  command=lambda cmd=command: self.button_clicked(cmd),
                                  width=100,
                                  height=35,
                                  font=config.FONTS['body'],
                                  fg_color=btn_color,
                                  hover_color=btn_color)
                btn.pack(side="left", padx=5)
        
        # Bind escape key
        self.overlay.bind("<Escape>", lambda e: self.close_modal())
        
    def button_clicked(self, command):
        if command:
            self.result = command()
        self.close_modal()
        
    def close_modal(self):
        self.overlay.grab_release()
        self.overlay.destroy()

class GameResultModal(CustomModal):
    def __init__(self, parent, result, is_blackjack=False):
        self.result_type = result
        self.is_blackjack = is_blackjack
        
        # Determine title, message, and type based on result
        if result == "win":
            if is_blackjack:
                title = "🃏 BLACKJACK! 🃏"
                message = "Natural 21! You win 3:2!"
                modal_type = "success"
            else:
                title = "🎉 YOU WIN! 🎉"
                message = "Congratulations! You beat the dealer!"
                modal_type = "success"
        elif result == "lose":
            title = "😔 DEALER WINS"
            message = "Better luck next time!"
            modal_type = "error"
        else:  # draw
            title = "🤝 PUSH (TIE)"
            message = "It's a tie! Your bet is returned."
            modal_type = "info"
            
        super().__init__(parent, title, message, modal_type)

class ConfirmationModal(CustomModal):
    def __init__(self, parent, title, message, on_confirm=None, on_cancel=None):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        buttons = [
            ("Cancel", self.cancel_clicked, "error"),
            ("Confirm", self.confirm_clicked, "success")
        ]
        
        super().__init__(parent, title, message, "question", buttons)
        
    def confirm_clicked(self):
        if self.on_confirm:
            return self.on_confirm()
        return True
        
    def cancel_clicked(self):
        if self.on_cancel:
            return self.on_cancel()
        return False

class InputModal:
    def __init__(self, parent, title, message, placeholder="", on_submit=None):
        self.parent = parent
        self.result = None
        self.on_submit = on_submit
        
        # Create overlay
        self.overlay = ctk.CTkFrame(parent, fg_color=("gray75", "gray25"))
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create modal window
        self.modal = ctk.CTkFrame(self.overlay,
                                corner_radius=15,
                                fg_color=config.COLORS['secondary'],
                                border_width=2,
                                border_color=config.COLORS['accent'])
        self.modal.place(relx=0.5, rely=0.5, anchor="center")
        
        self.setup_input_modal(title, message, placeholder)
        
        # Make modal grab focus
        self.overlay.grab_set()
        self.entry.focus_set()
        
    def setup_input_modal(self, title, message, placeholder):
        # Header
        header_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        header_frame.pack(pady=(20, 10), padx=20)
        
        icon_label = ctk.CTkLabel(header_frame,
                                text="💬",
                                font=('Segoe UI', 32),
                                text_color=config.COLORS['accent'])
        icon_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame,
                                 text=title,
                                 font=config.FONTS['subtitle'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack()
        
        # Message
        if message:
            message_label = ctk.CTkLabel(self.modal,
                                       text=message,
                                       font=config.FONTS['body'],
                                       text_color=config.COLORS['text_secondary'],
                                       wraplength=300)
            message_label.pack(pady=(0, 15), padx=20)
        
        # Input field
        self.entry = ctk.CTkEntry(self.modal,
                                width=250,
                                height=35,
                                font=config.FONTS['body'],
                                placeholder_text=placeholder)
        self.entry.pack(pady=(0, 20), padx=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        button_frame.pack(pady=(0, 20), padx=20)
        
        cancel_btn = ctk.CTkButton(button_frame,
                                 text="Cancel",
                                 command=self.cancel_clicked,
                                 width=100,
                                 height=35,
                                 font=config.FONTS['body'],
                                 fg_color=config.COLORS['danger'],
                                 hover_color=config.COLORS['danger'])
        cancel_btn.pack(side="left", padx=(0, 10))
        
        submit_btn = ctk.CTkButton(button_frame,
                                 text="Submit",
                                 command=self.submit_clicked,
                                 width=100,
                                 height=35,
                                 font=config.FONTS['body'],
                                 fg_color=config.COLORS['success'],
                                 hover_color=config.COLORS['success'])
        submit_btn.pack(side="left")
        
        # Bind keys
        self.entry.bind("<Return>", lambda e: self.submit_clicked())
        self.overlay.bind("<Escape>", lambda e: self.cancel_clicked())
        
    def submit_clicked(self):
        value = self.entry.get().strip()
        if value and self.on_submit:
            result = self.on_submit(value)
            if result:  # Only close if submission was successful
                self.result = value
                self.close_modal()
        elif value:
            self.result = value
            self.close_modal()
            
    def cancel_clicked(self):
        self.result = None
        self.close_modal()
        
    def close_modal(self):
        self.overlay.grab_release()
        self.overlay.destroy()

# Convenience functions for easy use
def show_info(parent, title, message):
    """Show an info modal"""
    return CustomModal(parent, title, message, "info")

def show_success(parent, title, message):
    """Show a success modal"""
    return CustomModal(parent, title, message, "success")

def show_warning(parent, title, message):
    """Show a warning modal"""
    return CustomModal(parent, title, message, "warning")

def show_error(parent, title, message):
    """Show an error modal"""
    return CustomModal(parent, title, message, "error")

def show_game_result(parent, result, is_blackjack=False):
    """Show game result modal"""
    return GameResultModal(parent, result, is_blackjack)

def show_confirmation(parent, title, message, on_confirm=None, on_cancel=None):
    """Show a confirmation modal"""
    return ConfirmationModal(parent, title, message, on_confirm, on_cancel)

def show_input(parent, title, message="", placeholder="", on_submit=None):
    """Show an input modal"""
    return InputModal(parent, title, message, placeholder, on_submit)