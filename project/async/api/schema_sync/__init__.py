import graphene

from api.schema_sync.queries import OctopusQuery


class Query(OctopusQuery):
    pass


schema_sync = graphene.Schema(query=Query)
