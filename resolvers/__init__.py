from ariadne import make_executable_schema
from .mutation import mutation
from .query import query
from .subscription import subscription
from .tokenpayload import tokenpayload

RESOLVERS = [
    mutation,
    query,
    subscription,
    tokenpayload
]
