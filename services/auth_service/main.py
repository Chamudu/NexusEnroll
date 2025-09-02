"""
Main Flask application for NexusEnroll Authentication Service
Provides REST API endpoints for authentication and user management
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from auth_service import AuthService
from user import User
from common.logger import log
from common.database import get_connection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the authentication service
auth_service = AuthService()

# Helper function to get user from session
def get_current_user(session_token):
    """Get current user from session token."""
    if not session_token:
        return None
    
    session_data = auth_service.validate_session(session_token)
    if not session_data:
        return None
    
    return auth_service.get_user_by_id(session_data["user_id"])

# Authentication endpoints

@app.route('/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and create session.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        # Authenticate user
        user = auth_service.authenticate_user(username, password)
        if not user:
            log(f"Failed login attempt for username: {username}")
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create session
        session_token = auth_service.create_session(user)
        
        log(f"Successful login for user: {username}")
        
        response_data = {
            "message": "Login successful",
            "session_token": session_token,
            "user": user.to_dict()
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        log(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    """
    Logout user by invalidating session.
    
    Headers:
    Authorization: Bearer <session_token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
        
        session_token = auth_header.split(' ')[1]
        
        # Invalidate session
        if auth_service.invalidate_session(session_token):
            log(f"User logged out successfully")
            return jsonify({"message": "Logout successful"}), 200
        else:
            return jsonify({"error": "Invalid session"}), 401
            
    except Exception as e:
        log(f"Logout error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/validate', methods=['GET'])
def validate_session():
    """
    Validate session token and return user info.
    
    Headers:
    Authorization: Bearer <session_token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
        
        session_token = auth_header.split(' ')[1]
        
        # Validate session
        session_data = auth_service.validate_session(session_token)
        if not session_data:
            return jsonify({"error": "Invalid or expired session"}), 401
        
        # Get user details
        user = auth_service.get_user_by_id(session_data["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "valid": True,
            "user": user.to_dict(),
            "session": {
                "created_at": session_data["created_at"].isoformat(),
                "last_accessed": session_data["last_accessed"].isoformat()
            }
        }), 200
        
    except Exception as e:
        log(f"Session validation error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# User management endpoints

@app.route('/auth/users', methods=['POST'])
def create_user():
    """
    Create a new user account.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string",
        "email": "string",
        "role": "student|faculty|administrator"
    }
    """
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            session_token = auth_header.split(' ')[1]
            current_user = get_current_user(session_token)
            
            if not current_user or not auth_service.authorize_action(current_user, "manage_users"):
                return jsonify({"error": "Insufficient permissions"}), 403
        else:
            # For demo purposes, allow user creation without auth
            # In production, this should require admin permissions
            pass
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Create user
        user = auth_service.create_user(data)
        log(f"New user created: {user.username} (role: {user.role})")
        
        return jsonify({
            "message": "User created successfully",
            "user": user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        log(f"User creation error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID."""
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user:
            return jsonify({"error": "Invalid session"}), 401
        
        # Users can view their own profile, admins can view any
        if current_user.user_id != user_id and not auth_service.authorize_action(current_user, "manage_users"):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        user = auth_service.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"user": user.to_dict()}), 200
        
    except Exception as e:
        log(f"Get user error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/users', methods=['GET'])
def list_users():
    """List all users (admin only)."""
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user or not auth_service.authorize_action(current_user, "manage_users"):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        # Get optional role filter
        role = request.args.get('role')
        users = auth_service.list_users(role)
        
        return jsonify({
            "users": [user.to_dict() for user in users],
            "total": len(users)
        }), 200
        
    except Exception as e:
        log(f"List users error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/users/<int:user_id>/deactivate', methods=['POST'])
def deactivate_user(user_id):
    """Deactivate a user account (admin only)."""
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user or not auth_service.authorize_action(current_user, "manage_users"):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        # Prevent self-deactivation
        if current_user.user_id == user_id:
            return jsonify({"error": "Cannot deactivate your own account"}), 400
        
        if auth_service.deactivate_user(user_id):
            log(f"User {user_id} deactivated by admin {current_user.username}")
            return jsonify({"message": "User deactivated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
        
    except Exception as e:
        log(f"Deactivate user error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/users/<int:user_id>/reset-password', methods=['POST'])
def reset_password(user_id):
    """Reset user password (admin only)."""
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user or not auth_service.authorize_action(current_user, "manage_users"):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        try:
            temp_password = auth_service.reset_password(user_id)
            log(f"Password reset for user {user_id} by admin {current_user.username}")
            
            return jsonify({
                "message": "Password reset successfully",
                "temporary_password": temp_password
            }), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        
    except Exception as e:
        log(f"Reset password error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/change-password', methods=['POST'])
def change_password():
    """
    Change current user's password.
    
    Expected JSON:
    {
        "current_password": "string",
        "new_password": "string"
    }
    """
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({"error": "Current password and new password are required"}), 400
        
        # Verify current password
        if not current_user.authenticate(current_password):
            return jsonify({"error": "Current password is incorrect"}), 400
        
        # Change password
        if current_user.change_password(new_password):
            log(f"Password changed for user {current_user.username}")
            return jsonify({"message": "Password changed successfully"}), 200
        else:
            return jsonify({"error": "New password does not meet requirements"}), 400
        
    except Exception as e:
        log(f"Change password error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Service status endpoints

@app.route('/auth/status', methods=['GET'])
def service_status():
    """Get authentication service status."""
    try:
        stats = auth_service.get_stats()
        return jsonify({
            "service": "NexusEnroll Authentication Service",
            "status": "running",
            "stats": stats
        }), 200
        
    except Exception as e:
        log(f"Status check error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/authorize', methods=['POST'])
def authorize():
    """
    Check if user is authorized for a specific action.
    
    Expected JSON:
    {
        "action": "string"
    }
    """
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
        session_token = auth_header.split(' ')[1]
        current_user = get_current_user(session_token)
        
        if not current_user:
            return jsonify({"error": "Invalid session"}), 401
        
        data = request.get_json()
        action = data.get('action') if data else None
        
        if not action:
            return jsonify({"error": "Action is required"}), 400
        
        is_authorized = auth_service.authorize_action(current_user, action)
        
        return jsonify({
            "authorized": is_authorized,
            "action": action,
            "user_role": current_user.role
        }), 200
        
    except Exception as e:
        log(f"Authorization check error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    log(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def serve_test_page():
    """Serve the web testing interface."""
    return send_from_directory('.', 'web_test.html')

@app.route('/test')
def test_interface():
    """Alternative route for the test interface."""
    return send_from_directory('.', 'web_test.html')

if __name__ == '__main__':
    log("Starting NexusEnroll Authentication Service...")
    print("NexusEnroll Authentication Service starting on port 5001")
    print("Available endpoints:")
    print("  POST /auth/login - User login")
    print("  POST /auth/logout - User logout")
    print("  GET  /auth/validate - Validate session")
    print("  POST /auth/users - Create user")
    print("  GET  /auth/users - List users")
    print("  GET  /auth/users/<id> - Get user by ID")
    print("  POST /auth/users/<id>/deactivate - Deactivate user")
    print("  POST /auth/users/<id>/reset-password - Reset password")
    print("  POST /auth/change-password - Change own password")
    print("  POST /auth/authorize - Check authorization")
    print("  GET  /auth/status - Service status")
    
    app.run(host='127.0.0.1', port=5001, debug=True)
