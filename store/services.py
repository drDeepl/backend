from collections import Counter
from datetime import timedelta, datetime
from typing import List, Dict

from django.db import transaction
from django.db.models import Q
from django.utils import timezone


from product.models import Product, ProductKit
from product.schemas import ProductOut, ProductKitOut
from store.exceptions import TeamHaveNot
from store.models import TeamProduct, TeamProductKit
from store.schemas import StoreProductOut, StoreProductKitOut

from team.models import Team


def add_product(team: Team, product: Product):
    TeamProduct.objects.create(team=team, product=product)


def add_product_kit(team: Team, product_kit: ProductKit):
    TeamProductKit.objects.create(team=team, product_kit=product_kit)


@transaction.atomic
def get_all_product_kits(team: Team) -> List[ProductKit]:
    print("get_all_product_kits", team)
    # check_products_created(team)
    
    all_product_kits: List[ProductKit] = list(map(lambda x: x.product_kit, TeamProductKit.objects.filter(team=team)))
    return all_product_kits
    # counter: Dict[ProductKit, int] = dict(Counter(all_product_kits))
    # return [StoreProductKitOut(product_kit=k, count=v) for k, v in counter.items()]



@transaction.atomic
def check_products_created(team: Team):
    team_product_kits: List[TeamProductKit] = TeamProductKit.objects.filter(team=team)
    
    print("CHECK PRODUCTS CREATED")
    
    for team_product_kit in team_product_kits:
        # INFO: заменил datetime.now() на timezone.now()
        # INFO: заменил >= на <=
        if team_product_kit.timestamp + timedelta(seconds=team_product_kit.product_kit.time) <= timezone.now():
            print("TIME OUT")
            for i in range(team_product_kit.product_kit.count):
                TeamProduct.objects.create(team=team_product_kit.team, product=team_product_kit.product_kit.product)
                
            team_product_kit.delete()



@transaction.atomic
def get_all_products(team: Team) -> List[StoreProductOut]:
    # check_products_created(team)

    all_products = list(map(lambda x: x.product, TeamProduct.objects.filter(team=team)))
    
    counter = dict(Counter(all_products))
    return [StoreProductOut(product=k, count=v) for k, v in counter.items()]


def count_product_kits(team: Team, product_kit: ProductKit) -> int:
    return TeamProductKit.objects.filter(Q(team=team) & Q(product_kit=product_kit)).count()


def count_products(team: Team, product: Product) -> int:
    return TeamProduct.objects.filter(Q(team=team) & Q(product=product)).count()


def remove_products(team: Team, team_product: TeamProduct, count: int):
    
    team_products = team_product.count
    
    if not team_products >= count:
        raise TeamHaveNot()
    team_product = TeamProduct.objects.filter(team=team, product=team_product.product).first()
    
    team_product.count -= count
    team_product.save()
    if team_products == count:
        team_product.delete()
    
    return


def remove_product_kit(team: Team, product_kit: ProductKit):
    TeamProductKit.objects.get(team=team, product_kit=product_kit).delete()
