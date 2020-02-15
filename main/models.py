from django.contrib.auth.models import User
from django.db import models


class AbonnementType(models.IntegerChoices):
    package1 = 1
    package2 = 2
    package3 = 3
    package4 = 4


class Abonnement(models.Model):
    package = models.IntegerField(choices=AbonnementType.choices, null=True)
    timestamp = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pacakge
