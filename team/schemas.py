from decimal import Decimal

from ninja import ModelSchema, Schema
from ninja_schema import model_validator

from team.models import Team


class TeamOutSchema(ModelSchema):
    class Config:
        model = Team
        model_fields = [
            "id", "name", "account"
        ]


class CreateTeamSchema(Schema):
    name: str
    balance: Decimal

    @model_validator('balance')
    def validate_positive_balance(cls, value_data: Decimal) -> Decimal:
        if value_data < 0:
            raise ValueError('Balance must be positive')
        return value_data


class PlayerTeamSchema(Schema):
    player_id: int
    team_id: int
