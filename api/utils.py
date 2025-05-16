import time

import jwt

def hash_data_with_token(data: dict, secret: str) -> str:
    """Creates a signed hash of user info with secret key"""

    # Set expiry time (5 minutes)
    data['exp'] = int(time.time()) + 300

    return jwt.encode(payload=data, key=secret, algorithm="HS256")