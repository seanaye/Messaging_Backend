from datetime import datetime
import math
import logging
from ariadne import MutationType
from authenticate import authenticate

# client = from_env()

# spigot = client.containers.get('spigot')

mutation = MutationType()


@mutation.field('addMessage')
@authenticate
async def r_message(_, info, chat, user, message):
    doc = {
        'message': str(message),
        'time': math.floor((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()),
        'user': str(user)
    }
    result = await info.context.chat_db[chat].insert_one(doc)
    if not (chat_channel := info.context.channels.get(chat)):
        chat_channel = {}
    active_users = chat_channel.keys()
    for user in active_users:
        await chat_channel[user].put(doc)
    return {
        'ok': True,
        'message': doc
    }


@mutation.field('createUser')
async def r_create_user(_, info, user, password):
    if await info.context.user_db['user'].find_one({'username': user}):
        return {
            'ok': False,
            'error': 'Username has been taken'
        }
    new_user = {
        'username': user,
        'pw_hash': info.context.hasher.hash(password)
    }
    reponse = await info.context.user_db['user'].insert_one(new_user)
    if reponse.inserted_id:
        return {
            'ok': True
        }
    return {
        'ok': False,
        'error': 'Error adding user to db'
    }
