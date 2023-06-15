from typing import List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from ninja_extra import permissions, http_post, http_get
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from offer.models import SaleOffer, PurchaseOffer
from offer.schemas import SaleOfferOut, SaleOfferPlace, SaleDoneOut, PurchaseOfferPlace, PurchaseOfferOut, \
    PurchaseDoneOut
from offer.services import find_active_sale_offers, acquire_sale_offer, find_active_purchase_offers, \
    acquire_purchase_offer
from product.models import ProductKit, Product
from user.models import User, Role
from user.utils import check_role
from team.models import Team


@api_controller('/offers/sale', tags=['Offer'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class SaleOfferController(ControllerBase):
    @http_post('/place', response=SaleOfferOut)
    def place_offer(self, payload: SaleOfferPlace):
        current_user = self.context.request.auth
        print("OFFER SALE PLACE current user")
        print(current_user.role)
        product_kit = get_object_or_404(ProductKit, id=payload.product_kit_id)
        team = get_object_or_404(Team, id=payload.team_id) # // FIX: ADDED
        result = SaleOffer.place(current_user, team,product_kit, payload.price)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'players',
            {'type': 'place.sale.offer', 'id': result.id}
        )
                    
        return result

    @http_get('/list', response=List[SaleOfferOut])
    def list_offers(self):
        offers_sale = find_active_sale_offers()
        return offers_sale

    @http_post('/acquire', response=SaleDoneOut)
    def acquire(self, offer_id: int, team_id: int):
        current_user: User = self.context.request.auth
        check_role(current_user, Role.PLAYER) # DEFAULT: PLAYER
        offer = get_object_or_404(SaleOffer, id=offer_id)
        team = get_object_or_404(Team, id=team_id)
        result = acquire_sale_offer(team, offer)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'players',
            {'type': 'acquired.sale.offer', 'id': offer_id}
        )
        for _i in range(0,5):
            print(channel_layer)
        return result


@api_controller('/offers/purchase', tags=['Offer'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class PurchaseOfferController(ControllerBase):
    @http_post('/place', response=PurchaseOfferOut)
    def place_offer(self, payload: PurchaseOfferPlace):
        current_user = self.context.request.auth
        product = get_object_or_404(Product, id=payload.product_id)

        result = PurchaseOffer.place(current_user, product, payload.count, payload.price)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'players',
            {'type': 'place.purchase.offer', 'id': result.id}
        )

        # FIX add return 
        return result

    @http_get('/list', response=List[PurchaseOfferOut])
    def list_offers(self):
        return find_active_purchase_offers()

    @http_post('/acquire', response=PurchaseDoneOut)
    def acquire(self, offer_id: int, team_id: int):
        current_user: User = self.context.request.auth
        
        check_role(current_user, Role.CUSTOMER) # DEFAULT: MANUFACTURER
        offer = get_object_or_404(PurchaseOffer, id=offer_id)

        # BEFORE result = acquire_purchase_offer(current_user.team, offer)
        result = acquire_purchase_offer(team_id, offer)
        

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'players',
            {'type': 'acquired.purchase.offer', 'id': offer_id}
        )

        return result
