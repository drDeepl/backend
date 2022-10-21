from decimal import Decimal
from typing import Any

from django.db import models

from account.models import Account
from account.services import create_account


class Team(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    account = models.OneToOneField(Account, models.CASCADE, null=False)

    @staticmethod
    def create(name: str, start_balance: Decimal):
        account = create_account(start_balance)
        team = Team(name=name, account=account)
        team.save()
        return team

    def rename(self, new_name: str):
        try:
            self.name = new_name
            self.save()
        except Exception:
            raise Exception('Cant rename')

    @staticmethod
    def remove(name: str) -> Any:
        Team.objects.filter(name=name).delete()
