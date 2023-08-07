from jwt import encode, decode

# CREATE TOKEN
def create_token(data: dict):
    token = encode(payload=data, key="smashmentor", algorithm="HS256")
    return token

# VALIDATE TOKEN
def validate_token(token: str) -> dict:
    data: dict = decode(token, key="smashmentor", algorithms=['HS256'])
    return data