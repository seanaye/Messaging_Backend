import logging
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from argon2 import PasswordHasher
import motor.motor_asyncio
from schema import SCHEMA
from jwt_client import JWT, ExpiredSignatureError
from keys import KEYS
from mixin import LoggerMixin


app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'], allow_methods=['*'])

class Context(LoggerMixin):
    def __init__(self):
        super().__init__()
        self.channels = {}
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')
        self.chat_db = self.client['chat']
        self.user_db = self.client['user']
        self.req = None
        self.hasher = PasswordHasher()
        self.jwt = JWT(refresh_secret=KEYS['refresh'], access_secret=KEYS['access'])

    def __call__(self, req):
        self.req = req
        return self

    def get_refresh_jwt(self):
        if not (token := self.req.headers.get('refresh')):
            return None
        try:
            return self.jwt.decode(token, kind='refresh')
        except Exception:
            return None

ctx = Context()

app.mount('/graphql', app=GraphQL(SCHEMA, context_value=ctx, debug=True))
