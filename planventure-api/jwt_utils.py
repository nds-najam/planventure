from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def generate_tokens(user_id, user_data=None):
    """
    Generate both access and refresh tokens for a user.
    
    Args:
        user_id (int): The user's ID
        user_data (dict): Optional additional data to include in token identity
    
    Returns:
        dict: A dictionary with 'access_token' and 'refresh_token'
    """
    identity = user_data or {'id': user_id}
    
    access_token = create_access_token(
        identity=identity,
        expires_delta=timedelta(hours=1)
    )
    
    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=timedelta(days=30)
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def create_new_access_token(user_id, user_data=None):
    """
    Create a new access token from a refresh token.
    
    Args:
        user_id (int): The user's ID
        user_data (dict): Optional additional data to include in token identity
    
    Returns:
        str: The new access token
    """
    identity = user_data or {'id': user_id}
    
    return create_access_token(
        identity=identity,
        expires_delta=timedelta(hours=1)
    )
