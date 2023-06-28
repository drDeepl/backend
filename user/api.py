from decimal import Decimal
from typing import List

from django.shortcuts import get_object_or_404
from ninja_extra import permissions, http_post, http_get, pagination, http_put, http_delete, status
from ninja_extra.controllers import Detail
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from account.services import create_account
from team.models import Team
from user.models import User, Role
from user.schemas import UserOut, UserNameOut, CreateUserSchema, UpdateUserSchema
from user.utils import check_admin
from ninja.pagination import paginate


@api_controller('/', tags=['User'])
class UserController(ControllerBase):
    @http_post('users', response=UserOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def create_user(self, payload: CreateUserSchema):
        check_admin(self.context)
        if payload.role == Role.PLAYER:
            team = get_object_or_404(Team, id=payload.team_id)
            user = User.objects.create_user(username=payload.username, email=payload.email, password=payload.password,
                                            role=payload.role, team=team, account=None)
            user.save()
        else:
            account = create_account(Decimal(1337228))
            account.is_unlimited = True
            account.save()
            user = User.objects.create_user(username=payload.username, email=payload.email, password=payload.password,
                                            role=payload.role, team=None, account=account)

        return user

    @http_get('users/{user_id}', response=UserOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def get_user(self, user_id: int):
        current_user: User = self.context.request.auth
        user = get_object_or_404(User, id=user_id)

        # if current_user != user:
            # check_admin(self.context)
        return user

    @http_get('users/name/{username}', response=UserOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def get_user_by_name(self, username: str):
        current_user: User = self.context.request.auth
        user = get_object_or_404(User, username=username)

        if current_user != user:
            check_admin(self.context)
        return user

    @http_get('users', response=List[UserOut], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    @paginate
    def list_users(self):
        check_admin(self.context)

        qs = User.objects.all()
        return qs
    

    @http_get('users-names-customer', response=List[UserNameOut], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    @paginate
    def list_names_customer(self):
        qs = User.objects.filter(role=Role.CUSTOMER)
        print()
        print()
        print()
        print()
        print(qs)
        return qs

    @http_put('users/{user_id}', response=UserOut, permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def update_user(self, user_id: int, payload: UpdateUserSchema):
        check_admin(self.context)

        user = get_object_or_404(User, id=user_id)
        user.first_name = payload.first_name
        user.last_name = payload.last_name
        user.role = payload.role
        team = get_object_or_404(Team, id=payload.team_id)
        user.team = team
        user.save()
        return user

    @http_delete('users/{user_id}',
                 permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def delete_user(self, user_id: int):
        check_admin(self.context)

        user = get_object_or_404(User, id=user_id)
        user.delete()
        return {"success": True}

    @http_delete('users/delete/{flag}',
                 permissions=[permissions.IsAuthenticated], auth=JWTAuth())
    def delete_users(self, flag: int):
        check_admin(self.context)
        if(flag):
            users = User.objects.filter(is_superuser=False)
            for user in users:
                user.delete()
            return {"success": True}
        else:
            return {"success": False}


    @http_get('roles', response=List[str])
    def get_roles(self):
        return [x.value for x in Role]
    

        
