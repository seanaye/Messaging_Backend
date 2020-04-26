from datetime import datetime
import math
from ariadne import QueryType
import motor
from argon2.exceptions import VerifyMismatchError
from authenticate import authenticate


query = QueryType()

@query.field('getMessages')
@authenticate
async def get_messages(_, info, chat, user, last):
    cursor = info.context.chat_db[chat].find()
    cursor.sort('time', -1).limit(last)
    return {
        'ok': True,
        'messages': [doc async for doc in cursor]
    }


@query.field('login')
async def r_login(_, info, user, password):
    if not (user_doc := await info.context.user_db['user'].find_one({'username': user})):
        return 'Invalid User'
    try:
        info.context.hasher.verify(user_doc['pw_hash'], password)
    except VerifyMismatchError:
        return 'Invalid Password'
    if info.context.hasher.check_needs_rehash(user_doc['pw_hash']):
        new_doc = user_doc.copy()
        new_doc['pw_hash'] = info.context.hasher.hash(password)
        await info.context.user_db['user'].replace_one({'_id': user_doc['_id']}, new_doc)
    
    return {
        'user': user_doc['username']
    }

@query.field('token')
async def r_token(_, info):
    if not (token := info.context.get_refresh_jwt()):
        return 'No valid token'
    return {
        'user': token['user']
    }
