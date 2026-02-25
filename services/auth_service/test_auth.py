"""
Test script for NexusEnroll Authentication Service
Demonstrates the functionality of the authentication system
"""

import sys
import os

# Add auth service to path
sys.path.append(os.path.dirname(__file__))

from auth_service import AuthService
from user import User

def test_authentication_service():
    """Test the authentication service functionality."""
    print("🔐 Testing NexusEnroll Authentication Service")
    print("=" * 50)
    
    # Initialize service
    auth_service = AuthService()
    
    # Test 1: User Authentication
    print("\n1. Testing User Authentication")
    print("-" * 30)
    
    # Test with default admin user
    user = auth_service.authenticate_user("admin", "admin123")
    if user:
        print(f"✅ Authentication successful for: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Permissions: {user.get_permissions()}")
    else:
        print("❌ Authentication failed")
    
    # Test with wrong password
    user = auth_service.authenticate_user("admin", "wrongpassword")
    if user:
        print("❌ Authentication should have failed")
    else:
        print("✅ Correctly rejected invalid password")
    
    # Test 2: User Creation
    print("\n2. Testing User Creation")
    print("-" * 30)
    
    try:
        new_user_data = {
            "username": "test_student",
            "password": "password123",
            "email": "test@nexusenroll.edu",
            "role": "student"
        }
        
        new_user = auth_service.create_user(new_user_data)
        print(f"✅ User created successfully: {new_user.username}")
        print(f"   User ID: {new_user.user_id}")
        print(f"   Role: {new_user.role}")
        
    except ValueError as e:
        print(f"❌ User creation failed: {e}")
    
    # Test duplicate username
    try:
        auth_service.create_user(new_user_data)
        print("❌ Should not allow duplicate usernames")
    except ValueError:
        print("✅ Correctly prevented duplicate username")
    
    # Test 3: Authorization
    print("\n3. Testing Authorization")
    print("-" * 30)
    
    admin_user = auth_service.get_user_by_username("admin")
    student_user = auth_service.get_user_by_username("test_student")
    faculty_user = auth_service.get_user_by_username("prof_smith")
    
    # Test admin permissions
    admin_actions = ["manage_users", "create_courses", "system_administration"]
    for action in admin_actions:
        if auth_service.authorize_action(admin_user, action):
            print(f"✅ Admin authorized for: {action}")
        else:
            print(f"❌ Admin should be authorized for: {action}")
    
    # Test student permissions
    student_actions = ["enroll_courses", "view_grades", "manage_users"]
    for action in student_actions:
        authorized = auth_service.authorize_action(student_user, action)
        if action == "manage_users":
            if not authorized:
                print(f"✅ Student correctly denied: {action}")
            else:
                print(f"❌ Student should not be authorized for: {action}")
        else:
            if authorized:
                print(f"✅ Student authorized for: {action}")
            else:
                print(f"❌ Student should be authorized for: {action}")
    
    # Test 4: Session Management
    print("\n4. Testing Session Management")
    print("-" * 30)
    
    # Create session
    session_token = auth_service.create_session(admin_user)
    print(f"✅ Session created: {session_token[:16]}...")
    
    # Validate session
    session_data = auth_service.validate_session(session_token)
    if session_data:
        print(f"✅ Session validated for user: {session_data['username']}")
    else:
        print("❌ Session validation failed")
    
    # Invalidate session
    if auth_service.invalidate_session(session_token):
        print("✅ Session invalidated successfully")
    else:
        print("❌ Session invalidation failed")
    
    # Try to validate invalidated session
    session_data = auth_service.validate_session(session_token)
    if not session_data:
        print("✅ Correctly rejected invalidated session")
    else:
        print("❌ Should not validate invalidated session")
    
    # Test 5: Password Management
    print("\n5. Testing Password Management")
    print("-" * 30)
    
    # Change password
    if student_user.change_password("newpassword123"):
        print("✅ Password changed successfully")
        
        # Test with new password
        if auth_service.authenticate_user("test_student", "newpassword123"):
            print("✅ Authentication with new password successful")
        else:
            print("❌ Authentication with new password failed")
        
        # Test with old password
        if not auth_service.authenticate_user("test_student", "password123"):
            print("✅ Correctly rejected old password")
        else:
            print("❌ Should reject old password")
    else:
        print("❌ Password change failed")
    
    # Test password reset
    try:
        temp_password = auth_service.reset_password(student_user.user_id)
        print(f"✅ Password reset successful. Temp password: {temp_password}")
        
        # Test with temporary password
        if auth_service.authenticate_user("test_student", temp_password):
            print("✅ Authentication with temporary password successful")
        else:
            print("❌ Authentication with temporary password failed")
            
    except ValueError as e:
        print(f"❌ Password reset failed: {e}")
    
    # Test 6: Account Lockout
    print("\n6. Testing Account Lockout")
    print("-" * 30)
    
    # Create a test user for lockout testing
    test_user_data = {
        "username": "lockout_test",
        "password": "password123",
        "email": "lockout@nexusenroll.edu",
        "role": "student"
    }
    
    lockout_user = auth_service.create_user(test_user_data)
    print(f"✅ Created test user for lockout: {lockout_user.username}")
    
    # Attempt multiple failed logins
    for i in range(6):  # Exceeds the 5-attempt limit
        result = auth_service.authenticate_user("lockout_test", "wrongpassword")
        if not result:
            print(f"   Failed attempt {i+1}/6")
    
    # Try with correct password (should be locked)
    result = auth_service.authenticate_user("lockout_test", "password123")
    if not result:
        print("✅ Account correctly locked after failed attempts")
    else:
        print("❌ Account should be locked")
    
    # Test 7: Service Statistics
    print("\n7. Testing Service Statistics")
    print("-" * 30)
    
    stats = auth_service.get_stats()
    print(f"✅ Service Statistics:")
    print(f"   Total users: {stats['total_users']}")
    print(f"   Active users: {stats['active_users']}")
    print(f"   Active sessions: {stats['active_sessions']}")
    print(f"   Locked accounts: {stats['locked_accounts']}")
    print(f"   Users by role: {stats['users_by_role']}")
    
    # Test 8: User Deactivation
    print("\n8. Testing User Deactivation")
    print("-" * 30)
    
    if auth_service.deactivate_user(lockout_user.user_id):
        print(f"✅ User {lockout_user.username} deactivated successfully")
        
        # Try to authenticate deactivated user
        result = auth_service.authenticate_user("lockout_test", "password123")
        if not result:
            print("✅ Correctly rejected deactivated user")
        else:
            print("❌ Should reject deactivated user")
    else:
        print("❌ User deactivation failed")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication Service Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_authentication_service()
