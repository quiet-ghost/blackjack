import tkinter as tk
from tkinter import ttk, messagebox
import config
from utils.auth import UserAuth

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack - Login")
        self.root.geometry("400x300")
        self.root.configure(bg=config.COLORS['background'])
        self.root.resizable(False, False)
        
        self.auth = UserAuth()
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=config.COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="🃏 BLACKJACK 🃏", 
                              font=config.FONTS['title'],
                              bg=config.COLORS['background'], 
                              fg=config.COLORS['text_primary'])
        title_label.pack(pady=20)
        
        login_frame = tk.Frame(main_frame, bg=config.COLORS['background'])
        login_frame.pack(expand=True)
        
        tk.Label(login_frame, text="Username:", font=config.FONTS['body'],
                bg=config.COLORS['background'], fg=config.COLORS['text_primary']).pack(pady=5)
        
        self.username_entry = tk.Entry(login_frame, font=config.FONTS['body'], width=20)
        self.username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", font=config.FONTS['body'],
                bg=config.COLORS['background'], fg=config.COLORS['text_primary']).pack(pady=5)
        
        self.password_entry = tk.Entry(login_frame, font=config.FONTS['body'], 
                                     width=20, show="*")
        self.password_entry.pack(pady=5)
        
        button_frame = tk.Frame(login_frame, bg=config.COLORS['background'])
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(button_frame, text="Login", command=self.login,
                             font=config.FONTS['button'], width=10,
                             bg=config.COLORS['button_bg'], fg=config.COLORS['button_text'])
        login_btn.pack(side='left', padx=5)
        
        register_btn = tk.Button(button_frame, text="Register", command=self.register,
                               font=config.FONTS['button'], width=10,
                               bg=config.COLORS['button_bg'], fg=config.COLORS['button_text'])
        register_btn.pack(side='left', padx=5)
        
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        success, message = self.auth.login_user(username, password)
        if success:
            self.root.destroy()
            self.start_game()
        else:
            messagebox.showerror("Login Failed", message)
            
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
            
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
            
        success, message = self.auth.register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Failed", message)
            
    def start_game(self):
        from gui.main_window import MainWindow
        game_window = MainWindow(self.auth)
        game_window.run()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login = LoginWindow()
    login.run()