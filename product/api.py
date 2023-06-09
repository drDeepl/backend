from typing import List

from django.shortcuts import get_object_or_404
from ninja_extra import permissions, http_post, http_get, pagination, http_put, http_delete, status,route
from ninja_extra.controllers import Detail
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from product.models import Product, ProductKit
from product.schemas import ProductOut, ProductIn, ProductKitOut, ProductKitIn
from user.utils import check_admin, check_role
from user.models import User, Role
from ninja.pagination import paginate


@api_controller('', tags=['Product'])
class ProductController(ControllerBase):
    @http_post('/products', response=ProductOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def create_product(self, payload: ProductIn):
        # check_admin(self.context)
        product = Product.objects.create(**payload.dict())
        return product

    @http_get('/products/{product_id}', response=ProductOut)
    def get_product(self, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        return product

    @http_get('/products', response=List[ProductOut])
    @paginate
    def list_products(self):
        qs = Product.objects.filter(is_deleted=False)
        return qs

    @http_get('/products/with/hide', response=List[ProductOut])
    def list_products_with_hide(self):
        qs = Product.objects.all()
        return list(qs)

    @http_put('/products/{product_id}', response=ProductOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def update_product(self, product_id: int, payload: ProductIn):
        check_admin(self.context)

        product = get_object_or_404(Product, id=product_id)
        for attr, value in payload.dict().items():
            setattr(product, attr, value)
        product.save()
        return product
    
    @http_get('/products/delete/{product_id}', response=ProductOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def set_state_deleted_product(self, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        product.is_deleted = True
        product.save()
        return product

    @http_delete('/products/{product_id}',
                 permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def delete_product(self, product_id: int):
        current_user: User = self.context.request.auth
        # check_role(current_user, Role.MANUFACTURER)
        check_admin(self.context)
        if(product_id == -1):
            products = Product.objects.all()
            for product in products:
                product.delete()

        else:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
        return {"success": True}


    @http_delete('/products/all/{flag}',
                 permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def delete_products(self, flag: int):
        
        if(flag):
            products = Product.objects.all()
            for product in products:
                product.delete()
                
        return {"success": True}


@api_controller('', tags=['Product Kit'])
class ProductKitController(ControllerBase):
    @http_post('/product-kits', response=ProductKitOut, auth=JWTAuth())
    def create_product_kit(self, payload: ProductKitIn):  # todo add handler wrong product id IntegrityError
        # check_admin(self.context)
        product_kit = ProductKit.objects.create(**payload.dict())

        return product_kit

    @http_get('/product-kits/{product_kit_id}', response=ProductKitOut)
    def get_product_kit(self, product_kit_id: int):
        product_kit = get_object_or_404(ProductKit, id=product_kit_id)
        return product_kit

    # // FIX: ADD FEATURE: get_product_name
    @http_get('/product-kits/product/{product_kit_id}', response=ProductOut)
    def get_product_from_product_kit(self, product_kit_id: int):
        product_kit = get_object_or_404(ProductKit, id=product_kit_id)

        product = product_kit.product
        return product
    
    @http_get('/product-kits/delete-for-product/{product_id}',)
    def set_deleted_product_kit_for_related_product(self, product_id: int):
        product_kits = ProductKit.objects.filter(product_id=product_id)
        for product_kit in product_kits:
            product_kit.is_deleted = True
            product_kit.save()
        

    @http_get('/product-kits', response=List[ProductKitOut])
    @paginate
    def list_products(self):
        qs = ProductKit.objects.filter(is_deleted=False)
        return qs

    @http_put('/product-kits/{product_kit_id}', response=ProductKitOut, auth=JWTAuth())
    def update_product_kit(self, product_kit_id: int, payload: ProductKitIn):
        check_admin(self.context)

        product_kit = get_object_or_404(ProductKit, id=product_kit_id)
        for attr, value in payload.dict().items():
            setattr(product_kit, attr, value)
        product_kit.save()
        return product_kit

    @http_get('/product-kits/delete/{product_kit_id}', response=ProductKitOut, auth=JWTAuth())
    def change_state_delete_product_kit(self, product_kit_id: int):
        product_kit = get_object_or_404(ProductKit, id=product_kit_id)
        product_kit.is_deleted = True
        product_kit.save()
        return product_kit

    

    @http_delete('/product-kits/{product_id}', auth=JWTAuth())
    def delete_product_kit(self, product_id: int):
        for _ in range(0,5):
            print()
        current_user: User = self.context.request.auth
        
        print(current_user.role)
        check_role(current_user, Role.MANUFACTURER)

        product_kit = get_object_or_404(ProductKit, id=product_id)
        product_kit.delete()
        return {"success": True}
