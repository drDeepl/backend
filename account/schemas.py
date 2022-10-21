from decimal import Decimal

from ninja import Schema, ModelSchema

from account.models import Transaction, Account


class AccountOut(ModelSchema):
    balance: Decimal

    class Config:
        model = Account
        model_fields = ['id', 'is_unlimited']


class TransactionOut(ModelSchema):
    class Config:
        model = Transaction
        model_fields = ['from_account', 'to_account', 'amount', 'timestamp']


class AccountAmountSchema(Schema):
    account_id: int
    amount: Decimal


class TransferSchema(Schema):
    account_id_from: int
    account_id_to: int
    amount: Decimal
