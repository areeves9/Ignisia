from flask_jwt_extended import get_jwt_identity
from flask_limiter.util import get_remote_address


def get_user_or_ip():
    """
    Returns the user identity from JWT if available,
    otherwise returns the remote IP address.
    This function is used as a key function for rate limiting.
    """
    try:
        return get_jwt_identity() or get_remote_address()
    except Exception:
        return get_remote_address()
