import asyncio
from ariadne import SubscriptionType
from jwt import ExpiredSignatureError, InvalidTokenError

subscription = SubscriptionType()

@subscription.source('subMessage')
async def r_generate_message(_, info, chat, accessToken):
    try:
        if not accessToken:
            yield {
                'ok': False,
                'error': 'Invalid auth token'
            }
            return
        user = info.context.jwt.decode(accessToken, kind='access').get('user')
    except ExpiredSignatureError:
        yield {
            'ok': False,
            'error': 'Token has expired'
        }
        return
    except InvalidTokenError:
        yield {
            'ok': False,
            'error': 'Invalid auth token'
        }
        return
    ac = info.context.channels
    if chat not in ac:
        ac[chat] = {}
    ac[chat][user] = asyncio.Queue()
    try:
        while True:
            msg = await ac[chat][user].get()
            yield {
                'ok': True,
                'message': msg
            }
    except GeneratorExit:
        del ac[chat][user]
        if len(ac[chat] == 0):
            del ac[chat]


@subscription.field('subMessage')
def r_sub_resolver(obj, info, chat, accessToken):
    info.context.logger.critical(obj)
    return obj


