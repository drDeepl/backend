from ninja import Schema

from product.schemas import ProductOut, ProductKitOut


class StoreProductOut(Schema):
    product: ProductOut
    count: int


class StoreProductKitOut(Schema):
    product_kit: ProductKitOut
    # count: int
