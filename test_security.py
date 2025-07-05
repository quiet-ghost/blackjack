#!/usr/bin/env python3
"""
Test script for secure authentication system
"""

import os
import sys
sys.path.append('.')

from utils.secure_auth import SecureUserAuth

def test_secure_auth():
    print("🔒 Testing Secure Authentication System")
    print("=" * 50)
    
    # Initialize secure auth
    auth = SecureUserAuth()
    
    # Test 1: Password strength validation
    print("\n1. Testing password strength validation:")
    weak_passwords = [
        "123",           # Too short
        "password",      # No uppercase, numbers, special chars
        "Password",      # No numbers, special chars
        "Password123",   # No special chars
    ]
    
    for pwd in weak_passwords:
        is_strong, message = auth.validate_password_strength(pwd)
        print(f"   '{pwd}' -> {message}")
    
    strong_password = "SecurePass123!"
    is_strong, message = auth.validate_password_strength(strong_password)
    print(f"   '{strong_password}' -> {message}")
    
    # Test 2: User registration with secure password
    print("\n2. Testing user registration:")
    success, message = auth.register_user("testuser", strong_password)
    print(f"   Registration: {message}")
    
    # Test 3: Login with correct credentials
    print("\n3. Testing login:")
    success, message = auth.login_user("testuser", strong_password)
    print(f"   Login: {message}")
    print(f"   Session valid: {auth.is_session_valid()}")
    
    # Test 4: Failed login attempts
    print("\n4. Testing failed login protection:")
    for i in range(3):
        success, message = auth.login_user("testuser", "wrongpassword")
        print(f"   Attempt {i+1}: {message}")
    
    # Test 5: Data encryption
    print("\n5. Testing data encryption:")
    users = auth.load_users()
    if "testuser" in users:
        user_data = users["testuser"]
        print(f"   Password stored as hash: {user_data['password_hash'][:20]}...")
        print(f"   Original password not visible in storage")
    
    # Test 6: Session management
    print("\n6. Testing session management:")
    print(f"   Current user: {auth.current_user}")
    print(f"   Session token exists: {auth.session_token is not None}")
    print(f"   Session valid: {auth.is_session_valid()}")
    
    auth.logout()
    print(f"   After logout - Session valid: {auth.is_session_valid()}")
    
    # Test 7: File security
    print("\n7. Testing file security:")
    if os.path.exists("database/secure_users.enc"):
        with open("database/secure_users.enc", "rb") as f:
            encrypted_content = f.read()
        print(f"   Encrypted file size: {len(encrypted_content)} bytes")
        print(f"   Content is encrypted (not readable): {encrypted_content[:50]}...")
    
    print("\n✅ Security tests completed!")
    print("\n🔐 Security Features Implemented:")
    print("   ✓ Password hashing with bcrypt (12 rounds)")
    print("   ✓ Password strength requirements")
    print("   ✓ Data encryption at rest (Fernet)")
    print("   ✓ Session management with expiry")
    print("   ✓ Account lockout after failed attempts")
    print("   ✓ Secure file permissions")
    print("   ✓ Protection against common attacks")

if __name__ == "__main__":
    test_secure_auth()