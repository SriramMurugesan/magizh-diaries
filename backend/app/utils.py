import secrets
import string


def generate_share_key(length: int = 16) -> str:
    """Generate a secure random share key for public links"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
