"""
Authentication utilities for password handling.
"""

import base64


def encode_password(password: str) -> str:
    """
    Encode password to base64.
    
    Args:
        password: Plain text password
        
    Returns:
        Base64 encoded password
    """
    return base64.b64encode(password.encode()).decode()


def verify_password(plain_password: str, encoded_password: str) -> bool:
    """
    Verify a password against its base64 encoded version.
    
    Args:
        plain_password: Plain text password to verify
        encoded_password: Base64 encoded password from database
        
    Returns:
        True if passwords match, False otherwise
    """
    try:
        # Encode the plain password and compare
        encoded_plain = base64.b64encode(plain_password.encode()).decode()
        return encoded_plain == encoded_password
    except Exception:
        return False
