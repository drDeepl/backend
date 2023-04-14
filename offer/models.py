from datetime import datetime
from decimal import Decimal
from enum import EnumMeta

from django.db import models

from account.models import Transaction
from offer.exceptions import OfferStateIsNotActiveException
from product.models import ProductKit, Product
from user.models import User, Role
from team.models import Team # // FIX: ADDED
from user.utils import check_role


class OfferState(EnumMeta):
    DONE = "Done"
    DELETED = "Deleted"
    ACTIVE = "Active"


#     Offer state map
#
# 0      => place   => Active
# Active => acquire => Done
# Active => remove  => Deleted
#


class Offer(models.Model):
    trader = models.ForeignKey(User, models.CASCADE)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=16, choices=[
        (tag, tag.value) for tag in OfferState
    ], default=OfferState.ACTIVE)

    def remove(self):
        if self.state != OfferState.ACTIVE:
            raise OfferStateIsNotActiveException()
        self.state = OfferState.DELETED

    class Meta:
        abstract = True


class SaleOffer(Offer):
    team = models.ForeignKey(Team, models.CASCADE) # // FIX: ADDED
    product_kit = models.ForeignKey(ProductKit, on_delete=models.CASCADE)

    @staticmethod
    def place(
            manufacturer: User,
            team_id: Team,# // FIX: ADDED
            product_kit: ProductKit,
            price: Decimal,
    ):
        check_role(manufacturer, Role.MANUFACTURER)

        return SaleOffer.objects.create(
            trader=manufacturer,
            team=team_id, # // FIX: ADDED
            product_kit=product_kit,
            price=price,
            state=OfferState.ACTIVE.value
        )


class PurchaseOffer(Offer):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    @staticmethod
    def place(
            customer: User,
            product: Product,
            count: int,
            price: Decimal
    ):

        check_role(customer, Role.PLAYER)
        print("PURCHASE OFFER PLACE")
        print("PURCHASE OFFER PLACE")
        print("PURCHASE OFFER PLACE")

        return PurchaseOffer.objects.create(
            trader=customer,
            product=product,
            count=count,
            price=price,
            state=OfferState.ACTIVE.value
        )


class SaleDone(models.Model):
    offer = models.OneToOneField(SaleOffer, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

    @property
    def product_kit(self) -> ProductKit:
        return self.offer.product_kit

    @property
    def start_time(self) -> datetime:
        return self.transaction.timestamp


class PurchaseDone(models.Model):
    offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
