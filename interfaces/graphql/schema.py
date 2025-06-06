from ariadne import load_schema_from_path, make_executable_schema

from interfaces.graphql.mutations import mutation
from interfaces.graphql.queries import query

type_defs = load_schema_from_path("interfaces/graphql/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)
