from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models

from account.models import Account
from team.models import Team


class Role(models.TextChoices):
    PLAYER = 'PLAYER', "Player"
    MANUFACTURER = 'MANUFACTURER', "Manufacturer"
    CUSTOMER = 'CUSTOMER', "Customer"


class User(AbstractUser):

    role = models.CharField(max_length=16,
                            choices=Role.choices,
                            default=Role.PLAYER)
    team = models.ForeignKey(Team, models.CASCADE, null=True)
    account = models.OneToOneField(Account, models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
