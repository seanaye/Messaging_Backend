from ariadne import make_executable_schema
from ariadne import load_schema_from_path
from resolvers import RESOLVERS

type_defs = load_schema_from_path('schema.graphql')

SCHEMA = make_executable_schema(type_defs, RESOLVERS)
