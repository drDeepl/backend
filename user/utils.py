from user.exceptions import UserIsNotAdminException, UserIsNotPlayerException, UserIsNotCustomerException, \
    UserIsNotManufacturerException
from user.models import Role, User


def check_role(user: User, role: Role):
    if user.role != role.value:
        if role == Role.PLAYER:
            raise UserIsNotPlayerException()
        elif role == Role.CUSTOMER:
            raise UserIsNotCustomerException()
        elif role == Role.MANUFACTURER:
            raise UserIsNotManufacturerException()
        else:
            print("Some dich role check")
            raise NotImplementedError()


def check_admin(context):
    user: User = context.request.auth
    if not user.is_superuser:
        raise UserIsNotAdminException()
