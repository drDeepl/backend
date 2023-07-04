from ninja import Schema, ModelSchema

from product.schemas import ProductOut, ProductKitOut
from store.models import TeamProduct


class StoreProductOut(ModelSchema):
    # product: ProductOut
    # count: int
    product_name: str
    class Config:
        model= TeamProduct
        model_fields = ['id','team','product','count']



class StoreProductKitOut(Schema):
    product_kit: ProductKitOut
    # count: int
