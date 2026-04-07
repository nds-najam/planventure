import re

def is_valid_email(email):
    """
    Validate email format using regex.
    
    Args:
        email (str): The email address to validate
    
    Returns:
        bool: True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password, min_length=8):
    """
    Validate password strength.
    
    Args:
        password (str): The password to validate
        min_length (int): Minimum password length (default: 8)
    
    Returns:
        bool: True if password meets requirements, False otherwise
    """
    if len(password) < min_length:
        return False
    
    # Check for at least one uppercase, one lowercase, and one digit
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit
