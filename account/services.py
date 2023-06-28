from decimal import Decimal
from typing import Optional

from account.exceptions import NotEnoughBalanceException, SameAccountException, AccountIsNoneException
from account.models import Account, Transaction


def transfer(account_from: Account, account_to: Account, amount: Decimal) -> Transaction:
    
    
    if account_from is None:
        raise AccountIsNoneException()
    if account_to is None:
        raise AccountIsNoneException()
    if account_from == account_to:
        raise SameAccountException()
    if (not account_from.is_unlimited) and (account_from.balance < amount):
        raise NotEnoughBalanceException()

    return Transaction.objects.create(
        from_account=account_from,
        to_account=account_to,
        amount=amount
    )


def emit(account: Account, amount: Decimal) -> Optional[Transaction]:
    if account.is_unlimited:
        return None
    return Transaction.objects.create(
        from_account=None,
        to_account=account,
        amount=amount
    )


def absorb(account: Account, amount: Decimal) -> Optional[Transaction]:
    if account.is_unlimited:
        return None
    if account.balance < amount:
        raise NotEnoughBalanceException()
    return Transaction.objects.create(
        from_account=account,
        to_account=None,
        amount=amount
    )


def create_account(balance: Decimal) -> Account:
    account = Account.objects.create()

    if balance > 0:
        emit(account, balance)

    return account

