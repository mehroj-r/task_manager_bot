import time

import jwt

def hash_data_with_token(data: dict, secret: str) -> str:
    """Creates a signed hash of user info with secret key"""

    # Set expiry time (30 secodns)
    data['exp'] = int(time.time()) + 30

    return jwt.encode(payload=data, key=secret, algorithm="HS256")