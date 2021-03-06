"""class for encoding and decoding jwt"""
from jwt import encode as encode_jwt
from jwt import decode as decode_jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

class JWT:
    """class that represents jwt encode/decoder"""
    def __init__(self, refresh_secret: str, access_secret: str):
        self._refresh_secret = refresh_secret
        self._access_secret = access_secret

    def encode(self, jsn: dict, kind: str) -> str:
        """encodes valid json as a jwt"""
        if kind == 'refresh':
            return encode_jwt(
                jsn,
                self._refresh_secret,
                algorithm='HS256'
            ).decode('utf-8')
        elif kind == 'access':
            return encode_jwt(
                jsn,
                self._access_secret,
                algorithm='HS256'
            ).decode('utf-8')
        raise ValueError('token kind must be either refresh or access')

    def decode(self, token: str, kind: str) -> dict:
        """decodes jwt into json(python dict)"""
        if kind == 'refresh':
            return decode_jwt(
                token.replace('Bearer ', '').encode('utf-8'),
                self._refresh_secret,
                algorithms=['HS256']
            )
        if kind == 'access':
            return decode_jwt(
                token.replace('Bearer ', '').encode('utf-8'),
                self._access_secret,
                algorithms=['HS256']
            )
        raise ValueError('token kind must be either refresh or access')
