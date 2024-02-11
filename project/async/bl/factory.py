import factory

from bl.models import Octopus, User, OctopusType, OctopusSeaFood, SeaFood


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'user{n}')

    class Meta:
        model = User


class OctopusTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OctopusType

    name = factory.Faker('first_name')


class OctopusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Octopus

    name = factory.Faker('first_name')
    age = factory.Faker('random_int', min=0, max=100)
    weight = factory.Faker('random_int', min=0, max=100)
    octopus_type = factory.SubFactory(OctopusTypeFactory)
    user = factory.SubFactory(UserFactory)


class SeaFoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SeaFood


class OctopusSeaFoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OctopusSeaFood

    octopus = factory.SubFactory(OctopusFactory)
    seafood = factory.SubFactory(SeaFoodFactory)
    weight = factory.Faker('random_int', min=0, max=100)
