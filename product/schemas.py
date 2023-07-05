from ninja import ModelSchema

from product.models import Product, ProductKit



class ProductOut(ModelSchema):
    class Config:
        model = Product
        model_fields = ['id', 'name', 'is_deleted']


class ProductIn(ModelSchema):
    class Config:
        model = Product
        model_exclude = ['id']


class ProductKitOut(ModelSchema):
    
    class Config:
        model = ProductKit
        model_fields = ['id', 'product', 'count', 'time', "is_deleted"]


class ProductKitIn(ModelSchema):
    product_id: int

    class Config:
        model = ProductKit
        model_exclude = ['id', 'product']
