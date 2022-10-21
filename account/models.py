from decimal import Decimal

from django.db import models


class Account(models.Model):
    is_unlimited = models.BooleanField(default=False)

    @property
    def balance(self) -> Decimal:
        # todo if transactions is empty
        credit: Decimal = sum(map(lambda x: x.amount, Transaction.objects.filter(from_account=self)))
        debit: Decimal = sum(map(lambda x: x.amount, Transaction.objects.filter(to_account=self)))
        return debit - credit  # todo about debit credit


class Transaction(models.Model):
    from_account = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True, related_name="from_account")
    to_account = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True, related_name="to_account")
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)

