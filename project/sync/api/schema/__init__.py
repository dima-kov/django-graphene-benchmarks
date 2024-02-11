import graphene

from api.schema.queries import OctopusQuery


class Query(OctopusQuery):
    pass


schema = graphene.Schema(query=Query)
