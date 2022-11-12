from typing import List

from django.shortcuts import get_object_or_404
from ninja_extra import permissions, http_post, http_get, pagination, http_put, http_delete, status
from ninja_extra.controllers import Detail
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from product.models import Product, ProductKit
from product.schemas import ProductOut, ProductIn, ProductKitOut, ProductKitIn
from user.utils import check_admin


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
    @pagination.paginate
    def list_products(self):
        qs = Product.objects.all()
        return qs

    @http_put('/products/{product_id}', response=ProductOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def update_product(self, product_id: int, payload: ProductIn):
        check_admin(self.context)

        product = get_object_or_404(Product, id=product_id)
        for attr, value in payload.dict().items():
            setattr(product, attr, value)
        product.save()
        return product

    @http_delete('/products/{product_id}',
                 permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def delete_product(self, product_id: int):
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

    @http_get('/product-kits', response=List[ProductKitOut])
    @pagination.paginate
    def list_products(self):
        qs = ProductKit.objects.all()
        return qs

    @http_put('/product-kits/{product_kit_id}', response=ProductKitOut, auth=JWTAuth())
    def update_product_kit(self, product_kit_id: int, payload: ProductKitIn):
        check_admin(self.context)

        product_kit = get_object_or_404(ProductKit, id=product_kit_id)
        for attr, value in payload.dict().items():
            setattr(product_kit, attr, value)
        product_kit.save()
        return product_kit

    @http_delete('/product-kits/{product_id}', auth=JWTAuth())
    def delete_product_kit(self, product_id: int):
        check_admin(self.context)

        product_kit = get_object_or_404(ProductKit, id=product_id)
        product_kit.delete()
        return {"success": True}
