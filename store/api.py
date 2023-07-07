from typing import List
from django.db import models
from ninja_extra import permissions, http_get, pagination
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from store.schemas import StoreProductOut, StoreProductKitOut
from product.schemas import ProductKitOut
from store.services import get_all_products, get_all_product_kits,check_products_created

from user.models import User
from store.models import TeamProduct, TeamProductKit


from user.utils import check_admin
from ninja.pagination import paginate

@api_controller('/store', tags=['Store'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class StoreController(ControllerBase):
    
    @http_get('team-product/{team_product_id}', response=StoreProductOut)
    def get_team_product(self, team_product_id: int):
        team_product = TeamProduct.objects.get(id=team_product_id)
        print(f"TEAM PRODUCT {team_product}")
        team_product.product_name = team_product.product.name
        return team_product

    @http_get('{team_id}/products/list', response=List[StoreProductOut])
    @paginate
    def list_products(self, team_id: int):
        current_user: User = self.context.request.auth
        team = current_user.team
        
        # if team.id != team_id:
        #     print("CHECK CURRENT TEAM")
        #     # check_admin(self.context)

        # FIX: Убрал получение списка продуктов команды текущего пользователя
        # FIX: Изменил на получение списка продуктов команды чей team_id указан в запросе
        def get_name_product(product):
            product.product_name = product.product.name
            return product
                
        return list(map(lambda product: get_name_product(product),TeamProduct.objects.filter(models.Q(team=team_id) & ~models.Q(count=0))))
        # return get_all_products(team_id)

    @http_get('{team_id}/product-kits/list', response=List[ProductKitOut])
    @paginate
    def list_product_kits(self, team_id: int):
        current_user: User = self.context.request.auth
        team = current_user.team
        return get_all_product_kits(team)

    @http_get('{team_id}/product-kits/check/{product_kit_id}')
    def check_created_products(self, team_id: int, product_kit_id: int):
        '''Function of create product for team '''
        current_user: User = self.context.request.auth
        team = current_user.team
        if team.id != team_id:
            
            check_admin(self.context)
        team_product_kit = TeamProductKit.objects.filter(product_kit=product_kit_id).first()
        
        
        
        teamProduct, createdTeamProduct = TeamProduct.objects.get_or_create(team=team, product=team_product_kit.product_kit.product)
        # if createdTeamProduct:
                     
        #     createdTeamProduct.count = team_product_kit.product_kit.count
        #     createdTeamProduct.save()
        # else:
        teamProduct.count += team_product_kit.product_kit.count
        teamProduct.save()
            
        team_product_kit.delete()
        return {'status': 'OK'}

    # FIX: Создал отдельный запрос для проверки готовности продуктов
    # @http_get('{team_id}/product-kits/check')
    
    # def check_created_products(self, team_id: int):
    #     current_user: User = self.context.request.auth
    #     team = current_user.team
    #     if team.id != team_id:
            
    #         check_admin(self.context)

        # return check_products_created(team)

    