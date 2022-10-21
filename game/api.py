from django.db import IntegrityError
from django.http import Http404
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from account.api import AccountController, TransactionController
from offer.api import SaleOfferController, PurchaseOfferController
from product.api import ProductController, ProductKitController
from store.api import StoreController
from team.api import TeamController
from user.api import UserController
from user.exceptions import UserIsNotAdminException

api = NinjaExtraAPI()


@api.exception_handler(Http404)
def not_fount_exceptions(request, exception):
    return api.create_response(
        request,
        {'message': "Not found"},
        status=404,
    )


@api.exception_handler(IntegrityError)
def integrity_error(request, exception):
    return api.create_response(
        request,
        {'message': "Error of creation (Integrity)"},
        status=400,
    )


@api.exception_handler(UserIsNotAdminException)
def not_admin_exceptions(request, exception):
    return api.create_response(
        request,
        {'message': "Not admin"},
        status=401,
    )


def on_exception(request, exception: Exception):
    return api.create_response(
        request,
        {'message': str(exception)},
        status=400,
    )


api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(ProductController, ProductKitController)
api.register_controllers(UserController)
api.register_controllers(AccountController, TransactionController)
api.register_controllers(SaleOfferController, PurchaseOfferController)
api.register_controllers(StoreController)
api.register_controllers(TeamController)
