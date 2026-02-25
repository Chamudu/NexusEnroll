"""
User class for NexusEnroll Authentication Service
Implements the User entity as defined in the class diagram
"""

import hashlib
import datetime
from typing import List, Optional


class User:
    """
    User entity representing all users in the NexusEnroll system.
    Serves as the base class for Student, Faculty, and Administrator.
    """
    
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str):
        """
        Initialize a new User instance.
        
        Args:
            user_id (int): Unique identifier for the user
            username (str): Unique username for login
            password (str): Plain text password (will be hashed)
            email (str): User's email address
            role (str): User role (student, faculty, administrator)
        """
        self.user_id = user_id
        self.username = username
        self.password_hash = self._hash_password(password)
        self.email = email
        self.role = role
        self.last_login: Optional[datetime.datetime] = None
        self.is_active = True
        self.created_at = datetime.datetime.now()
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        # In production, use bcrypt or scrypt with salt
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, password: str) -> bool:
        """
        Authenticate user with provided password.
        
        Args:
            password (str): Password to verify
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.is_active:
            return False
        
        hashed_input = self._hash_password(password)
        return hashed_input == self.password_hash
    
    def change_password(self, new_password: str) -> bool:
        """
        Change user's password.
        
        Args:
            new_password (str): New password
            
        Returns:
            bool: True if password changed successfully
        """
        if len(new_password) < 8:  # Basic password policy
            return False
        
        self.password_hash = self._hash_password(new_password)
        return True
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
    
    def get_permissions(self) -> List[str]:
        """
        Get user permissions based on role.
        
        Returns:
            List[str]: List of permissions for this user
        """
        base_permissions = ["view_profile", "change_password"]
        
        role_permissions = {
            "student": [
                "enroll_courses", 
                "view_grades", 
                "view_schedule",
                "drop_courses"
            ],
            "faculty": [
                "view_roster",
                "submit_grades", 
                "manage_courses",
                "view_student_records"
            ],
            "administrator": [
                "manage_users",
                "create_courses", 
                "generate_reports",
                "system_administration",
                "override_enrollment"
            ]
        }
        
        return base_permissions + role_permissions.get(self.role, [])
    
    def to_dict(self) -> dict:
        """
        Convert user object to dictionary representation.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "permissions": self.get_permissions()
        }
    
    def __str__(self) -> str:
        """String representation of the user."""
        return f"User(id={self.user_id}, username='{self.username}', role='{self.role}')"
    
    def __repr__(self) -> str:
        """Detailed representation of the user."""
        return (f"User(user_id={self.user_id}, username='{self.username}', "
                f"email='{self.email}', role='{self.role}', is_active={self.is_active})")
