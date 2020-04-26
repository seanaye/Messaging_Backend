from datetime import datetime, timedelta
from ariadne import ObjectType

tokenpayload = ObjectType('TokenPayload')

@tokenpayload.field('ok')
def r_ok(obj, _):
    if isinstance(obj, dict):
        return True
    return False

@tokenpayload.field('error')
def r_error(obj, _):
    if isinstance(obj, str):
        return obj
    return None

@tokenpayload.field('access')
def r_access(obj, info):
    if isinstance(obj, dict):
        access = {
            **obj,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        return info.context.jwt.encode(access, kind='access')
    return None

@tokenpayload.field('refresh')
def r_refresh(obj, info):
    if isinstance(obj, dict):
        refresh = {
            ** obj,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        return info.context.jwt.encode(refresh, kind='refresh')
    return None