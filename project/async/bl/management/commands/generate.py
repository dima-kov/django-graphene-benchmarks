# command to generate a series of Octopus objects into DB
# 1_000_000 Octopus objects
# 1_000 User objects
# 10 OctopusType objects
# 70 SeaFood objects
# use factories to generate the objects
# use bulk_create to insert the objects into the DB
# first create the OctopusType and SeaFood objects
# then create the User objects
# then create the Octopus objects (use existing randomly chosen User, OctopusType, and SeaFood objects)
import random

from django.core.management import BaseCommand

from bl.factory import UserFactory, OctopusFactory
from bl.models import OctopusType, SeaFood, User, Octopus, OctopusSeaFood


class Command(BaseCommand):
    help = 'Generate Octopus objects into the database'

    def handle(self, *args, **kwargs):
        # delete all existing objects
        Octopus.objects.all().delete()
        User.objects.all().delete()
        OctopusType.objects.all().delete()
        SeaFood.objects.all().delete()
        self.stdout.write('Deleted all existing octopuses, users, octopus types, and sea foods')

        types = OctopusType.objects.bulk_create(
            [OctopusType(name=f'OctopusType {i}') for i in range(10)]
        )
        foods = SeaFood.objects.bulk_create(
            [SeaFood(name=f'SeaFood {i}') for i in range(70)]
        )
        users = User.objects.bulk_create(
            [UserFactory.build() for _ in range(1_000)]
        )

        chunks = 4
        chunk_len = 50_000
        for i in range(chunks):
            octopuses = Octopus.objects.bulk_create([
                OctopusFactory.build(
                    user=random.choice(users),
                    octopus_type=random.choice(types)
                ) for _ in range(chunk_len)
            ])
            self.stdout.write(f'Generated {len(octopuses)} octopuses')
            # generate OctopusSeaFood objects
            # up to 10 SeaFood objects per Octopus
            # use bulk_create to insert into DB
            # use Factory to generate the objects
            oct_food = []
            for _oct in octopuses:
                for _ in range(random.randint(1, 10)):
                    oct_food.append(
                        OctopusSeaFood(
                            octopus=_oct,
                            seafood=random.choice(foods),
                            weight=random.randint(1, 100)
                        )
                    )
            oct_foods = OctopusSeaFood.objects.bulk_create(oct_food)
            self.stdout.write(f'Generated {len(oct_foods)} octopus sea foods')
        self.stdout.write(self.style.SUCCESS('Successfully generated octopuses'))
