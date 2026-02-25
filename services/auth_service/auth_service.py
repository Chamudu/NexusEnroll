"""
AuthService class for NexusEnroll Authentication Service
Implements authentication and authorization logic as defined in the class diagram
"""

import datetime
import secrets
import string
from typing import Dict, Optional, List
from user import User


class AuthService:
    """
    Authentication Service responsible for managing user authentication,
    authorization, and user lifecycle operations.
    """
    
    def __init__(self):
        """Initialize the AuthService with empty collections."""
        self.users: Dict[str, User] = {}  # username -> User mapping
        self.sessions: Dict[str, dict] = {}  # session_token -> session_data mapping
        self.failed_attempts: Dict[str, dict] = {}  # username -> attempt_data mapping
        self._user_id_counter = 1
        
        # Initialize with some default users for testing
        self._create_default_users()
    
    def _create_default_users(self) -> None:
        """Create default users for testing purposes."""
        # Create default admin
        admin_user = User(
            user_id=1,
            username="admin",
            password="admin123",
            email="admin@nexusenroll.edu",
            role="administrator"
        )
        self.users["admin"] = admin_user
        
        # Create default faculty
        faculty_user = User(
            user_id=2,
            username="prof_smith",
            password="faculty123",
            email="smith@nexusenroll.edu",
            role="faculty"
        )
        self.users["prof_smith"] = faculty_user
        
        # Create default student
        student_user = User(
            user_id=3,
            username="alice_student",
            password="student123",
            email="alice@nexusenroll.edu",
            role="student"
        )
        self.users["alice_student"] = student_user
        
        self._user_id_counter = 4
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        Args:
            username (str): Username to authenticate
            password (str): Password to verify
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        # Check if user exists
        user = self.users.get(username)
        if not user:
            self.track_login_attempt(username, success=False, reason="user_not_found")
            return None
        
        # Check for account lockout due to failed attempts
        if self._is_account_locked(username):
            self.track_login_attempt(username, success=False, reason="account_locked")
            return None
        
        # Verify password
        if user.authenticate(password):
            user.update_last_login()
            self._reset_failed_attempts(username)
            self.track_login_attempt(username, success=True)
            return user
        else:
            self.track_login_attempt(username, success=False, reason="invalid_password")
            return None
    
    def authorize_action(self, user: User, action: str) -> bool:
        """
        Authorize if user can perform a specific action.
        
        Args:
            user (User): User requesting authorization
            action (str): Action to authorize
            
        Returns:
            bool: True if user is authorized, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        user_permissions = user.get_permissions()
        return action in user_permissions
    
    def create_user(self, user_data: dict) -> User:
        """
        Create a new user account.
        
        Args:
            user_data (dict): User information including username, password, email, role
            
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If username already exists or required fields are missing
        """
        required_fields = ["username", "password", "email", "role"]
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        username = user_data["username"]
        if username in self.users:
            raise ValueError(f"Username '{username}' already exists")
        
        # Validate role
        valid_roles = ["student", "faculty", "administrator"]
        if user_data["role"] not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
        
        # Create new user
        user = User(
            user_id=self._user_id_counter,
            username=username,
            password=user_data["password"],
            email=user_data["email"],
            role=user_data["role"]
        )
        
        self.users[username] = user
        self._user_id_counter += 1
        
        return user
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id (int): ID of user to deactivate
            
        Returns:
            bool: True if user was deactivated, False if user not found
        """
        for user in self.users.values():
            if user.user_id == user_id:
                user.deactivate()
                # Invalidate all sessions for this user
                self._invalidate_user_sessions(user_id)
                return True
        return False
    
    def reset_password(self, user_id: int) -> str:
        """
        Reset user password to a randomly generated one.
        
        Args:
            user_id (int): ID of user whose password to reset
            
        Returns:
            str: New temporary password
            
        Raises:
            ValueError: If user not found
        """
        for user in self.users.values():
            if user.user_id == user_id:
                # Generate temporary password
                temp_password = self._generate_temporary_password()
                user.change_password(temp_password)
                return temp_password
        
        raise ValueError(f"User with ID {user_id} not found")
    
    def track_login_attempt(self, username: str, success: bool = True, reason: str = "") -> None:
        """
        Track login attempts for security monitoring.
        
        Args:
            username (str): Username attempting login
            success (bool): Whether login was successful
            reason (str): Reason for failure if unsuccessful
        """
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {
                "attempts": [],
                "locked_until": None
            }
        
        attempt_data = {
            "timestamp": datetime.datetime.now(),
            "success": success,
            "reason": reason
        }
        
        self.failed_attempts[username]["attempts"].append(attempt_data)
        
        # If failed attempt, check if we need to lock account
        if not success:
            recent_failures = self._count_recent_failures(username)
            if recent_failures >= 5:  # Lock after 5 failed attempts
                lockout_duration = datetime.timedelta(minutes=15)
                self.failed_attempts[username]["locked_until"] = (
                    datetime.datetime.now() + lockout_duration
                )
    
    def create_session(self, user: User) -> str:
        """
        Create a new session for authenticated user.
        
        Args:
            user (User): Authenticated user
            
        Returns:
            str: Session token
        """
        session_token = self._generate_session_token()
        session_data = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "created_at": datetime.datetime.now(),
            "last_accessed": datetime.datetime.now()
        }
        
        self.sessions[session_token] = session_data
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[dict]:
        """
        Validate a session token.
        
        Args:
            session_token (str): Session token to validate
            
        Returns:
            Optional[dict]: Session data if valid, None otherwise
        """
        session_data = self.sessions.get(session_token)
        if not session_data:
            return None
        
        # Check if session is expired (24 hours)
        session_age = datetime.datetime.now() - session_data["created_at"]
        if session_age > datetime.timedelta(hours=24):
            del self.sessions[session_token]
            return None
        
        # Update last accessed time
        session_data["last_accessed"] = datetime.datetime.now()
        return session_data
    
    def invalidate_session(self, session_token: str) -> bool:
        """
        Invalidate a session (logout).
        
        Args:
            session_token (str): Session token to invalidate
            
        Returns:
            bool: True if session was invalidated, False if not found
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id (int): User ID to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        for user in self.users.values():
            if user.user_id == user_id:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username (str): Username to search for
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return self.users.get(username)
    
    def list_users(self, role: Optional[str] = None) -> List[User]:
        """
        List all users, optionally filtered by role.
        
        Args:
            role (Optional[str]): Role to filter by
            
        Returns:
            List[User]: List of users
        """
        users = list(self.users.values())
        if role:
            users = [user for user in users if user.role == role]
        return users
    
    # Private helper methods
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is currently locked."""
        if username not in self.failed_attempts:
            return False
        
        locked_until = self.failed_attempts[username].get("locked_until")
        if locked_until and datetime.datetime.now() < locked_until:
            return True
        
        return False
    
    def _count_recent_failures(self, username: str, window_minutes: int = 15) -> int:
        """Count failed login attempts in recent time window."""
        if username not in self.failed_attempts:
            return 0
        
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=window_minutes)
        recent_attempts = [
            attempt for attempt in self.failed_attempts[username]["attempts"]
            if attempt["timestamp"] > cutoff_time and not attempt["success"]
        ]
        
        return len(recent_attempts)
    
    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed login attempts for user."""
        if username in self.failed_attempts:
            self.failed_attempts[username] = {
                "attempts": [],
                "locked_until": None
            }
    
    def _invalidate_user_sessions(self, user_id: int) -> None:
        """Invalidate all sessions for a specific user."""
        sessions_to_remove = [
            token for token, data in self.sessions.items()
            if data["user_id"] == user_id
        ]
        
        for token in sessions_to_remove:
            del self.sessions[token]
    
    def _generate_session_token(self) -> str:
        """Generate a secure random session token."""
        return secrets.token_urlsafe(32)
    
    def _generate_temporary_password(self) -> str:
        """Generate a temporary password."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(12))
    
    def get_stats(self) -> dict:
        """
        Get authentication service statistics.
        
        Returns:
            dict: Service statistics
        """
        active_users = sum(1 for user in self.users.values() if user.is_active)
        active_sessions = len(self.sessions)
        locked_accounts = sum(
            1 for data in self.failed_attempts.values()
            if data.get("locked_until") and datetime.datetime.now() < data["locked_until"]
        )
        
        return {
            "total_users": len(self.users),
            "active_users": active_users,
            "active_sessions": active_sessions,
            "locked_accounts": locked_accounts,
            "users_by_role": {
                role: len([u for u in self.users.values() if u.role == role])
                for role in ["student", "faculty", "administrator"]
            }
        }
