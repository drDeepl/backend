from typing import List

from django.db import transaction
from django.core.paginator import Paginator

from account.services import transfer
from offer.models import SaleOffer, PurchaseOffer, OfferState, SaleDone, PurchaseDone
from store.services import add_product_kit, remove_products
from team.models import Team
from user.models import User



def find_active_sale_offers() -> List[SaleOffer]:
    return list(SaleOffer.objects.filter(state=OfferState.ACTIVE.value))

def find_active_sale_offers_for_team(team_id:int) -> List[SaleOffer]:
    return list(SaleOffer.objects.filter(state=OfferState.ACTIVE.value, team=team_id))

def find_await_sale_offers_for_team(team_id:int) -> List[SaleOffer]:
    return list(SaleOffer.objects.filter(state=OfferState.AWAIT.value, team=team_id))



def find_done_sale_offers() -> List[SaleOffer]:
    # offers_sale_done = SaleOffer.objects.filter(state=OfferState.DONE.value)
    
    # return list(Paginator(offers_sale_done, count_elements_on_page).get_page(page))
    return list(SaleOffer.objects.filter(state=OfferState.DONE.value))
    
def find_done_purchase_offers() -> List[PurchaseOffer]:
    return list(PurchaseOffer.objects.filter(state=OfferState.DONE.value))


def find_active_purchase_offers() -> List[PurchaseOffer]:
    return list(PurchaseOffer.objects.filter(state=OfferState.ACTIVE.value))

def find_active_purchase_offers_for_customer(customer_id:int) -> List[PurchaseOffer]:
    return list(PurchaseOffer.objects.filter(state=OfferState.AWAIT.value, to_customer=customer_id))

@transaction.atomic
def acquire_sale_offer(team: Team, offer: SaleOffer) -> SaleDone:
    seller = User.objects.get(id=offer.trader.id)
    account_transaction = transfer(team.account, seller.account, offer.price)
    offer.state = OfferState.DONE.value
    sale = SaleDone.objects.create(offer=offer, transaction=account_transaction)
    offer.save()
    add_product_kit(team, offer.product_kit)

    return sale


@transaction.atomic
def acquire_purchase_offer(customer: User, offer: PurchaseOffer) -> PurchaseDone:
    trader = User.objects.get(id=offer.trader.id)
    account_trader = Team.objects.get(id=trader.team.id)
    print(f"TRADER ACCOUNT {account_trader.account}")
    
    account_transaction = transfer(customer.account, account_trader.account, offer.price)
    offer.state = OfferState.DONE.value
    purchase = PurchaseDone.objects.create(offer=offer, transaction=account_transaction)
    offer.save()
    
    remove_products(team=trader.team, product=offer.product, count=offer.count)
    
    return purchase

# todo add background task (product_kit -> products)
