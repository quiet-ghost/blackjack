import customtkinter as ctk
import config

class FloatingModal:
    def __init__(self, parent, title, message, modal_type="info", buttons=None, width=350, height=200):
        self.parent = parent
        self.result = None
        self.modal_type = modal_type
        
        # Create semi-transparent overlay (only covers content, not full screen)
        self.overlay = ctk.CTkFrame(parent, 
                                  fg_color=("gray75", "gray25"),
                                  corner_radius=0)
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create floating modal window (smaller, centered)
        self.modal = ctk.CTkToplevel(parent)
        self.modal.title("")
        self.modal.geometry(f"{width}x{height}")
        self.modal.resizable(False, False)
        self.modal.transient(parent)
        self.modal.grab_set()
        
        # Remove window decorations for cleaner look
        self.modal.overrideredirect(True)
        
        # Center the modal on parent window
        self.center_modal(width, height)
        
        # Style the modal
        self.modal.configure(fg_color=config.COLORS['secondary'])
        
        self.setup_modal(title, message, buttons)
        
        # Bind click on overlay to close (optional)
        self.overlay.bind("<Button-1>", lambda e: self.close_modal())
        
    def center_modal(self, width, height):
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.modal.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_modal(self, title, message, buttons):
        # Main container with border
        main_frame = ctk.CTkFrame(self.modal, 
                                corner_radius=15,
                                fg_color=config.COLORS['secondary'],
                                border_width=2,
                                border_color=config.COLORS['accent'])
        main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
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
        
        # Header with close button
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        # Close button (X)
        close_btn = ctk.CTkButton(header_frame,
                                text="✕",
                                command=self.close_modal,
                                width=25,
                                height=25,
                                font=('Segoe UI', 12, 'bold'),
                                fg_color="transparent",
                                text_color=config.COLORS['text_muted'],
                                hover_color=config.COLORS['danger'])
        close_btn.pack(side="right")
        
        # Icon and title
        icon_title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icon_title_frame.pack(side="left", fill="x", expand=True)
        
        icon_label = ctk.CTkLabel(icon_title_frame,
                                text=icon,
                                font=('Segoe UI', 20),
                                text_color=color)
        icon_label.pack(side="left", padx=(0, 8))
        
        title_label = ctk.CTkLabel(icon_title_frame,
                                 text=title,
                                 font=config.FONTS['body'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(side="left")
        
        # Message
        if message:
            message_label = ctk.CTkLabel(main_frame,
                                       text=message,
                                       font=config.FONTS['small'],
                                       text_color=config.COLORS['text_secondary'],
                                       wraplength=280)
            message_label.pack(pady=(5, 15), padx=15)
        
        # Buttons
        if buttons is None:
            # Default OK button
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(pady=(0, 15), padx=15)
            
            ok_btn = ctk.CTkButton(button_frame,
                                 text="OK",
                                 command=self.close_modal,
                                 width=80,
                                 height=30,
                                 font=config.FONTS['small'],
                                 fg_color=color,
                                 hover_color=color)
            ok_btn.pack()
        else:
            # Custom buttons
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(pady=(0, 15), padx=15)
            
            for i, (text, command, style) in enumerate(buttons):
                btn_color = colors.get(style, config.COLORS['accent'])
                btn = ctk.CTkButton(button_frame,
                                  text=text,
                                  command=lambda cmd=command: self.button_clicked(cmd),
                                  width=80,
                                  height=30,
                                  font=config.FONTS['small'],
                                  fg_color=btn_color,
                                  hover_color=btn_color)
                btn.pack(side="left", padx=3)
        
        # Bind escape key
        self.modal.bind("<Escape>", lambda e: self.close_modal())
        self.modal.focus_set()
        
    def button_clicked(self, command):
        if command:
            self.result = command()
        self.close_modal()
        
    def close_modal(self):
        self.overlay.destroy()
        self.modal.destroy()

class FloatingGameResult(FloatingModal):
    def __init__(self, parent, result, is_blackjack=False):
        # Determine modal content
        if result == "win":
            if is_blackjack:
                title = "BLACKJACK!"
                message = "Natural 21! You win 3:2!"
                modal_type = "success"
                width, height = 300, 180
            else:
                title = "YOU WIN!"
                message = "Congratulations! You beat the dealer!"
                modal_type = "success"
                width, height = 320, 180
        elif result == "lose":
            title = "DEALER WINS"
            message = "Better luck next time!"
            modal_type = "error"
            width, height = 300, 180
        else:  # draw
            title = "PUSH (TIE)"
            message = "It's a tie! Your bet is returned."
            modal_type = "info"
            width, height = 320, 180
            
        super().__init__(parent, title, message, modal_type, width=width, height=height)

class FloatingConfirmation(FloatingModal):
    def __init__(self, parent, title, message, on_confirm=None, on_cancel=None):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        buttons = [
            ("Cancel", self.cancel_clicked, "error"),
            ("Confirm", self.confirm_clicked, "success")
        ]
        
        super().__init__(parent, title, message, "question", buttons, width=350, height=200)
        
    def confirm_clicked(self):
        if self.on_confirm:
            return self.on_confirm()
        return True
        
    def cancel_clicked(self):
        if self.on_cancel:
            return self.on_cancel()
        return False

class FloatingInput:
    def __init__(self, parent, title, message="", placeholder="", on_submit=None):
        self.parent = parent
        self.result = None
        self.on_submit = on_submit
        
        # Create semi-transparent overlay
        self.overlay = ctk.CTkFrame(parent, 
                                  fg_color=("gray75", "gray25"),
                                  corner_radius=0)
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create floating modal
        self.modal = ctk.CTkToplevel(parent)
        self.modal.title("")
        self.modal.geometry("350x220")
        self.modal.resizable(False, False)
        self.modal.transient(parent)
        self.modal.grab_set()
        self.modal.overrideredirect(True)
        
        # Center the modal
        self.center_modal(350, 220)
        
        self.setup_input_modal(title, message, placeholder)
        
    def center_modal(self, width, height):
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.modal.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_input_modal(self, title, message, placeholder):
        # Main container
        main_frame = ctk.CTkFrame(self.modal,
                                corner_radius=15,
                                fg_color=config.COLORS['secondary'],
                                border_width=2,
                                border_color=config.COLORS['accent'])
        main_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        close_btn = ctk.CTkButton(header_frame,
                                text="✕",
                                command=self.cancel_clicked,
                                width=25,
                                height=25,
                                font=('Segoe UI', 12, 'bold'),
                                fg_color="transparent",
                                text_color=config.COLORS['text_muted'],
                                hover_color=config.COLORS['danger'])
        close_btn.pack(side="right")
        
        title_label = ctk.CTkLabel(header_frame,
                                 text=f"💬 {title}",
                                 font=config.FONTS['body'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(side="left")
        
        # Message
        if message:
            message_label = ctk.CTkLabel(main_frame,
                                       text=message,
                                       font=config.FONTS['small'],
                                       text_color=config.COLORS['text_secondary'],
                                       wraplength=280)
            message_label.pack(pady=(5, 10), padx=15)
        
        # Input field
        self.entry = ctk.CTkEntry(main_frame,
                                width=280,
                                height=35,
                                font=config.FONTS['body'],
                                placeholder_text=placeholder)
        self.entry.pack(pady=(0, 15), padx=15)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 15), padx=15)
        
        cancel_btn = ctk.CTkButton(button_frame,
                                 text="Cancel",
                                 command=self.cancel_clicked,
                                 width=80,
                                 height=30,
                                 font=config.FONTS['small'],
                                 fg_color=config.COLORS['danger'],
                                 hover_color=config.COLORS['danger'])
        cancel_btn.pack(side="left", padx=(0, 5))
        
        submit_btn = ctk.CTkButton(button_frame,
                                 text="Submit",
                                 command=self.submit_clicked,
                                 width=80,
                                 height=30,
                                 font=config.FONTS['small'],
                                 fg_color=config.COLORS['success'],
                                 hover_color=config.COLORS['success'])
        submit_btn.pack(side="left")
        
        # Bind keys and focus
        self.entry.bind("<Return>", lambda e: self.submit_clicked())
        self.modal.bind("<Escape>", lambda e: self.cancel_clicked())
        self.entry.focus_set()
        
    def submit_clicked(self):
        value = self.entry.get().strip()
        if value and self.on_submit:
            result = self.on_submit(value)
            if result:
                self.result = value
                self.close_modal()
        elif value:
            self.result = value
            self.close_modal()
            
    def cancel_clicked(self):
        self.result = None
        self.close_modal()
        
    def close_modal(self):
        self.overlay.destroy()
        self.modal.destroy()

# Convenience functions
def show_floating_info(parent, title, message):
    return FloatingModal(parent, title, message, "info", width=300, height=160)

def show_floating_success(parent, title, message):
    return FloatingModal(parent, title, message, "success", width=300, height=160)

def show_floating_warning(parent, title, message):
    return FloatingModal(parent, title, message, "warning", width=300, height=160)

def show_floating_error(parent, title, message):
    return FloatingModal(parent, title, message, "error", width=300, height=160)

def show_floating_game_result(parent, result, is_blackjack=False):
    return FloatingGameResult(parent, result, is_blackjack)

def show_floating_confirmation(parent, title, message, on_confirm=None, on_cancel=None):
    return FloatingConfirmation(parent, title, message, on_confirm, on_cancel)

def show_floating_input(parent, title, message="", placeholder="", on_submit=None):
    return FloatingInput(parent, title, message, placeholder, on_submit)