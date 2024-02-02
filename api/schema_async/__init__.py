import graphene

from api.schema_async.queries import OctopusQuery


class Query(OctopusQuery):
    pass


schema_async = graphene.Schema(query=Query)
