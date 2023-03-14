from typing import Optional

from ninja import ModelSchema
from ninja_schema import model_validator

from user.models import User, Role


class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = [
            "id", "last_login", "username", "first_name", "last_name", "email", "date_joined", "role", "team",
            "account", "is_superuser",
        ]


class UserNameOut(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "username",]

class UpdateUserSchema(ModelSchema):
    team_id: int

    class Config:
        model = User
        model_fields = ["role", "first_name", "last_name"]

    @model_validator('role')
    def validate_role(cls, value_data: str) -> str:
        if value_data not in Role._value2member_map_:
            raise ValueError('Role does not exist')
        return value_data


class CreateUserSchema(ModelSchema):
    password: str
    team_id: Optional[int]

    class Config:
        model = User
        model_fields = ["username", "first_name", "last_name", "email", "role"]

    @model_validator('username')
    def validate_unique_username(cls, value_data: str) -> str:
        if User.objects.filter(username__icontains=value_data).exists():
            raise ValueError('Username exists')
        return value_data

    @model_validator('role')
    def validate_role(cls, value_data: str) -> str:
        if value_data not in Role._value2member_map_:
            raise ValueError('Role does not exist')
        return value_data
