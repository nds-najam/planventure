from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hash a plaintext password using werkzeug's secure hashing.
    
    Args:
        password (str): The plaintext password to hash
    
    Returns:
        str: The hashed password with salt
    """
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(hashed_password, password):
    """
    Verify a plaintext password against a hashed password.
    
    Args:
        hashed_password (str): The stored hashed password
        password (str): The plaintext password to verify
    
    Returns:
        bool: True if the password matches, False otherwise
    """
    return check_password_hash(hashed_password, password)
