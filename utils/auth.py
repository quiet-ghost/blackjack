import os
import json
from pathlib import Path

class UserAuth:
    def __init__(self):
        self.users_file = Path("database/users.json")
        self.current_user = None
        self.ensure_users_file()
        
    def ensure_users_file(self):
        if not self.users_file.exists():
            self.users_file.parent.mkdir(exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
                
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
            
    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
            
    def register_user(self, username, password):
        users = self.load_users()
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            'password': password,
            'chips': 1000,
            'games_played': 0,
            'games_won': 0,
            'games_lost': 0,
            'games_drawn': 0
        }
        self.save_users(users)
        return True, "User registered successfully"
        
    def login_user(self, username, password):
        users = self.load_users()
        if username not in users:
            return False, "Username not found"
        
        if users[username]['password'] != password:
            return False, "Invalid password"
            
        self.current_user = username
        return True, "Login successful"
        
    def get_user_data(self, username=None):
        if not username:
            username = self.current_user
        if not username:
            return None
            
        users = self.load_users()
        return users.get(username)
        
    def update_user_data(self, data, username=None):
        if not username:
            username = self.current_user
        if not username:
            return False
            
        users = self.load_users()
        if username in users:
            users[username].update(data)
            self.save_users(users)
            return True
        return False
        
    def logout(self):
        self.current_user = None
