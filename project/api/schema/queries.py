import graphene
from graphene_django import DjangoObjectType
from bl.models import Octopus, User, OctopusType, SeaFood


class OctopusNode(DjangoObjectType):
    class Meta:
        model = Octopus
        fields = [
            'id',
            'name',
            'age',
            'weight',
            'octopus_type',
            'sea_food',
            'user'
        ]


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'password'
        ]


class OctopusTypeNode(DjangoObjectType):
    class Meta:
        model = OctopusType
        fields = ['id', 'name']


class SeaFoodNode(DjangoObjectType):
    class Meta:
        model = SeaFood
        fields = ['id', 'name']


class OctopusQuery(graphene.ObjectType):
    octopuses = graphene.List(OctopusNode)
    octopus = graphene.Field(OctopusNode, id=graphene.Int())

    def resolve_octopuses(self, info, **kwargs):
        return Octopus.objects.all()[:500]

    def resolve_octopus(self, info, id):
        return Octopus.objects.get(pk=id)
