from typing import List

from ninja_extra import permissions, http_get, pagination
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from store.schemas import StoreProductOut, StoreProductKitOut
from store.services import get_all_products, get_all_product_kits
from user.models import User
from user.utils import check_admin


@api_controller('/store', tags=['Store'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class StoreController(ControllerBase):
    @http_get('{team_id}/products/list', response=List[StoreProductOut])
    @pagination.paginate
    def list_products(self, team_id: int):
        current_user: User = self.context.request.auth
        team = current_user.team

        if team.id != team_id:
            print("CHECK CURRENT TEAM")
            check_admin(self.context)

        return get_all_products(team)

    @http_get('{team_id}/product-kits/list', response=List[StoreProductKitOut])
    @pagination.paginate
    def list_product_kits(self, team_id: int):
        current_user: User = self.context.request.auth
        team = current_user.team

        if team.id != team_id:
            print("CHECK CURRENT TEAM")
            # check_admin(self.context)

        return get_all_product_kits(team)
