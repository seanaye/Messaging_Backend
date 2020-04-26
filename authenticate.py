import functools
from typing import Callable, Optional, Any
from inspect import iscoroutinefunction
from jwt_client import decode_jwt, ExpiredSignatureError, InvalidTokenError
from keys import KEYS

# TODO create websocket authenticator. Headers not present on wss ?
def authenticate(func: Callable) -> Callable:
    @functools.wraps(func)
    async def authwrapper(obj: Optional[dict], info, **kwargs: Any) -> dict:
        try:
            if not (u := info.context.req.headers.get('Authorization')):
                return {
                    'ok': False,
                    'error': 'Invalid auth token'
                }
            token = decode_jwt(u.replace('Bearer ', ''), KEYS['access'], algorithms='HS256')
            if iscoroutinefunction(func):
                return await func(obj, info, **kwargs, user=token['user'])
            else:
                return func(obj, info, **kwargs, user=token['user'])
        except ExpiredSignatureError:
            return {
                'ok': False,
                'error': 'Token has expired'
            }
        except InvalidTokenError:
            return {
                'ok': False,
                'error': 'Invalid auth token'
            }
    return authwrapper