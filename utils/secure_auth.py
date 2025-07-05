import os
import json
import bcrypt
import secrets
import time
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureUserAuth:
    def __init__(self):
        self.users_file = Path("database/secure_users.enc")
        self.key_file = Path("database/.key")
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
        self.SESSION_DURATION = 3600  # 1 hour
        
        self.ensure_encryption_key()
        self.ensure_users_file()
        
    def ensure_encryption_key(self):
        """Generate or load encryption key for data at rest"""
        if not self.key_file.exists():
            # Generate a new key
            key = Fernet.generate_key()
            self.key_file.parent.mkdir(exist_ok=True)
            
            # Store key securely (in production, use environment variables or key management)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            
            # Set restrictive permissions (Unix-like systems)
            try:
                os.chmod(self.key_file, 0o600)
            except:
                pass  # Windows doesn't support chmod
                
        with open(self.key_file, 'rb') as f:
            self.encryption_key = f.read()
            
        self.cipher = Fernet(self.encryption_key)
        
    def ensure_users_file(self):
        """Create encrypted users file if it doesn't exist"""
        if not self.users_file.exists():
            self.users_file.parent.mkdir(exist_ok=True)
            empty_data = {}
            self.save_users(empty_data)
            
    def load_users(self):
        """Load and decrypt user data"""
        try:
            if not self.users_file.exists():
                return {}
                
            with open(self.users_file, 'rb') as f:
                encrypted_data = f.read()
                
            if not encrypted_data:
                return {}
                
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
            
    def save_users(self, users):
        """Encrypt and save user data"""
        try:
            json_data = json.dumps(users, indent=2).encode()
            encrypted_data = self.cipher.encrypt(json_data)
            
            with open(self.users_file, 'wb') as f:
                f.write(encrypted_data)
                
            # Set restrictive permissions
            try:
                os.chmod(self.users_file, 0o600)
            except:
                pass  # Windows doesn't support chmod
                
        except Exception as e:
            print(f"Error saving users: {e}")
            
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)  # Strong salt
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
    def validate_password_strength(self, password):
        """Validate password meets security requirements"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
            
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
            
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
            
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
            
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"
            
        return True, "Password is strong"
        
    def generate_session_token(self):
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
        
    def register_user(self, username, password):
        """Register new user with secure password storage"""
        # Validate username
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
            
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Username can only contain letters, numbers, hyphens, and underscores"
            
        # Validate password strength
        is_strong, message = self.validate_password_strength(password)
        if not is_strong:
            return False, message
            
        users = self.load_users()
        if username.lower() in [u.lower() for u in users.keys()]:
            return False, "Username already exists"
            
        # Hash password and store user
        hashed_password = self.hash_password(password)
        
        users[username] = {
            'password_hash': hashed_password,
            'chips': 1000,
            'games_played': 0,
            'games_won': 0,
            'games_lost': 0,
            'games_drawn': 0,
            'created_at': time.time(),
            'last_login': None,
            'login_attempts': 0,
            'locked_until': None
        }
        
        self.save_users(users)
        return True, "User registered successfully"
        
    def login_user(self, username, password):
        """Login user with secure authentication"""
        users = self.load_users()
        
        # Find user (case-insensitive)
        actual_username = None
        for stored_username in users.keys():
            if stored_username.lower() == username.lower():
                actual_username = stored_username
                break
                
        if not actual_username:
            return False, "Invalid username or password"
            
        user_data = users[actual_username]
        
        # Check if account is locked
        if user_data.get('locked_until') and time.time() < user_data['locked_until']:
            remaining = int(user_data['locked_until'] - time.time())
            return False, f"Account locked. Try again in {remaining} seconds"
            
        # Verify password
        if not self.verify_password(password, user_data['password_hash']):
            # Increment failed attempts
            user_data['login_attempts'] = user_data.get('login_attempts', 0) + 1
            
            # Lock account after 5 failed attempts
            if user_data['login_attempts'] >= 5:
                user_data['locked_until'] = time.time() + 300  # 5 minutes
                self.save_users(users)
                return False, "Too many failed attempts. Account locked for 5 minutes"
                
            self.save_users(users)
            return False, "Invalid username or password"
            
        # Successful login
        user_data['login_attempts'] = 0
        user_data['locked_until'] = None
        user_data['last_login'] = time.time()
        self.save_users(users)
        
        # Create session
        self.current_user = actual_username
        self.session_token = self.generate_session_token()
        self.session_expiry = time.time() + self.SESSION_DURATION
        
        return True, "Login successful"
        
    def is_session_valid(self):
        """Check if current session is valid"""
        if not self.session_token or not self.session_expiry:
            return False
        return time.time() < self.session_expiry
        
    def refresh_session(self):
        """Refresh current session"""
        if self.is_session_valid():
            self.session_expiry = time.time() + self.SESSION_DURATION
            return True
        return False
        
    def get_user_data(self, username=None):
        """Get user data (excluding sensitive information)"""
        if not self.is_session_valid():
            return None
            
        if not username:
            username = self.current_user
        if not username:
            return None
            
        users = self.load_users()
        user_data = users.get(username)
        
        if user_data:
            # Return copy without sensitive data
            safe_data = user_data.copy()
            safe_data.pop('password_hash', None)
            safe_data.pop('login_attempts', None)
            safe_data.pop('locked_until', None)
            return safe_data
            
        return None
        
    def update_user_data(self, data, username=None):
        """Update user data (excluding sensitive fields)"""
        if not self.is_session_valid():
            return False
            
        if not username:
            username = self.current_user
        if not username:
            return False
            
        # Prevent updating sensitive fields
        forbidden_fields = {'password_hash', 'login_attempts', 'locked_until', 'created_at'}
        safe_data = {k: v for k, v in data.items() if k not in forbidden_fields}
        
        users = self.load_users()
        if username in users:
            users[username].update(safe_data)
            self.save_users(users)
            return True
        return False
        
    def change_password(self, old_password, new_password):
        """Change user password"""
        if not self.is_session_valid() or not self.current_user:
            return False, "Session expired"
            
        users = self.load_users()
        user_data = users.get(self.current_user)
        
        if not user_data:
            return False, "User not found"
            
        # Verify old password
        if not self.verify_password(old_password, user_data['password_hash']):
            return False, "Current password is incorrect"
            
        # Validate new password
        is_strong, message = self.validate_password_strength(new_password)
        if not is_strong:
            return False, message
            
        # Update password
        user_data['password_hash'] = self.hash_password(new_password)
        self.save_users(users)
        
        return True, "Password changed successfully"
        
    def logout(self):
        """Logout user and invalidate session"""
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
        
    def migrate_from_old_auth(self, old_auth_file):
        """Migrate users from old plain-text system"""
        try:
            with open(old_auth_file, 'r') as f:
                old_users = json.load(f)
                
            users = self.load_users()
            migrated_count = 0
            
            for username, old_data in old_users.items():
                if username not in users:
                    # Hash the old plain-text password
                    hashed_password = self.hash_password(old_data['password'])
                    
                    users[username] = {
                        'password_hash': hashed_password,
                        'chips': old_data.get('chips', 1000),
                        'games_played': old_data.get('games_played', 0),
                        'games_won': old_data.get('games_won', 0),
                        'games_lost': old_data.get('games_lost', 0),
                        'games_drawn': old_data.get('games_drawn', 0),
                        'created_at': time.time(),
                        'last_login': None,
                        'login_attempts': 0,
                        'locked_until': None
                    }
                    migrated_count += 1
                    
            self.save_users(users)
            return True, f"Migrated {migrated_count} users successfully"
            
        except Exception as e:
            return False, f"Migration failed: {e}"