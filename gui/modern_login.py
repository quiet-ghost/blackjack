import customtkinter as ctk
import config
from utils.secure_auth import SecureUserAuth
from gui.floating_modals import show_floating_error, show_floating_success, show_floating_info

class ModernLoginWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        self.root.minsize(400, 500)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"500x600+{x}+{y}")
        
        self.auth = SecureUserAuth()
        
        # Auto-migrate from old system if needed
        self.migrate_old_users()
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header section
        header_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['secondary'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Casino title with cards
        title_label = ctk.CTkLabel(header_frame, 
                                 text="🃏 BLACKJACK CASINO 🃏",
                                 font=config.FONTS['title'],
                                 text_color=config.COLORS['text_primary'])
        title_label.pack(pady=30)
        
        subtitle_label = ctk.CTkLabel(header_frame,
                                    text="Welcome to the ultimate card game experience",
                                    font=config.FONTS['body'],
                                    text_color=config.COLORS['text_secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # Login form
        form_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['secondary'])
        form_frame.pack(fill="x", pady=(0, 20))
        
        form_title = ctk.CTkLabel(form_frame,
                                text="🎮 Player Login",
                                font=config.FONTS['subtitle'],
                                text_color=config.COLORS['text_primary'])
        form_title.pack(pady=(30, 20))
        
        # Username field
        username_label = ctk.CTkLabel(form_frame,
                                    text="Username",
                                    font=config.FONTS['body'],
                                    text_color=config.COLORS['text_secondary'])
        username_label.pack(pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(form_frame,
                                         width=300,
                                         height=40,
                                         font=config.FONTS['body'],
                                         placeholder_text="Enter your username",
                                         corner_radius=8)
        self.username_entry.pack(pady=(0, 15))
        
        # Password field
        password_label = ctk.CTkLabel(form_frame,
                                    text="Password",
                                    font=config.FONTS['body'],
                                    text_color=config.COLORS['text_secondary'])
        password_label.pack(pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(form_frame,
                                         width=300,
                                         height=40,
                                         font=config.FONTS['body'],
                                         placeholder_text="Enter your password",
                                         show="*",
                                         corner_radius=8)
        self.password_entry.pack(pady=(0, 25))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 30))
        
        self.login_btn = ctk.CTkButton(button_frame,
                                     text="🎯 Login & Play",
                                     command=self.login,
                                     width=140,
                                     height=45,
                                     font=config.FONTS['button'],
                                     fg_color=config.COLORS['accent'],
                                     hover_color=config.COLORS['accent_hover'],
                                     corner_radius=8)
        self.login_btn.pack(side="left", padx=(0, 10))
        
        self.register_btn = ctk.CTkButton(button_frame,
                                        text="📝 Register",
                                        command=self.register,
                                        width=140,
                                        height=45,
                                        font=config.FONTS['button'],
                                        fg_color=config.COLORS['warning'],
                                        hover_color=config.COLORS['warning'],
                                        corner_radius=8)
        self.register_btn.pack(side="left")
        
        # Features section
        features_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=config.COLORS['primary'])
        features_frame.pack(fill="x")
        
        features_title = ctk.CTkLabel(features_frame,
                                    text="🌟 Game Features",
                                    font=config.FONTS['subtitle'],
                                    text_color=config.COLORS['text_primary'])
        features_title.pack(pady=(20, 10))
        
        features = [
            "💰 Virtual chip system with persistent balance",
            "📊 Detailed statistics and achievements",
            "🎴 Professional card animations",
            "🏆 Leaderboard and progress tracking"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(features_frame,
                                       text=feature,
                                       font=config.FONTS['small'],
                                       text_color=config.COLORS['text_secondary'])
            feature_label.pack(pady=2)
        
        features_frame.pack_configure(pady=(0, 0))
        ctk.CTkLabel(features_frame, text="", height=20).pack()  # Spacer
        
        # Password requirements info
        req_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=config.COLORS['primary'])
        req_frame.pack(fill="x", pady=(10, 0))
        
        req_title = ctk.CTkLabel(req_frame,
                               text="🔒 Password Requirements",
                               font=config.FONTS['small'],
                               text_color=config.COLORS['text_primary'])
        req_title.pack(pady=(10, 5))
        
        requirements = [
            "• At least 8 characters long",
            "• Contains uppercase and lowercase letters", 
            "• Contains at least one number",
            "• Contains at least one special character"
        ]
        
        for req in requirements:
            req_label = ctk.CTkLabel(req_frame,
                                   text=req,
                                   font=('Segoe UI', 10),
                                   text_color=config.COLORS['text_muted'])
            req_label.pack(pady=1)
            
        ctk.CTkLabel(req_frame, text="", height=10).pack()  # Spacer
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            show_floating_error(self.root, "Error", "Please enter both username and password")
            return
            
        success, message = self.auth.login_user(username, password)
        if success:
            self.root.destroy()
            self.start_game()
        else:
            show_floating_error(self.root, "Login Failed", message)
            
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            show_floating_error(self.root, "Error", "Please enter both username and password")
            return
            
        if len(username) < 3:
            show_floating_error(self.root, "Error", "Username must be at least 3 characters")
            return
            
        # Password strength validation is now handled by SecureUserAuth
            
        success, message = self.auth.register_user(username, password)
        if success:
            show_floating_success(self.root, "Success", message)
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
        else:
            show_floating_error(self.root, "Registration Failed", message)
            
    def start_game(self):
        from gui.modern_main import ResponsiveMainWindow
        game_window = ResponsiveMainWindow(self.auth)
        game_window.run()
        
    def migrate_old_users(self):
        """Migrate users from old plain-text system"""
        import os
        old_file = "database/users.json"
        if os.path.exists(old_file):
            success, message = self.auth.migrate_from_old_auth(old_file)
            if success and "0 users" not in message:
                show_floating_info(self.root, "Migration Complete", 
                                 f"Your account has been upgraded with enhanced security.\n{message}")
                # Backup and remove old file
                import shutil
                shutil.move(old_file, f"{old_file}.backup")
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = ModernLoginWindow()
    login.run()