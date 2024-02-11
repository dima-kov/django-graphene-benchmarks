from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class OctopusType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SeaFood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OctopusSeaFood(models.Model):
    octopus = models.ForeignKey('Octopus', on_delete=models.CASCADE)
    seafood = models.ForeignKey('SeaFood', on_delete=models.CASCADE)
    weight = models.FloatField()

    def __str__(self):
        return f'{self.octopus.name} - {self.seafood.name}'


class Octopus(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    octopus_type = models.ForeignKey(OctopusType, on_delete=models.CASCADE)
    seafood = models.ManyToManyField(SeaFood, through=OctopusSeaFood)

    def __str__(self):
        return self.name
