from typing import List, Optional

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja_extra import permissions, http_post, http_get, pagination
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_jwt.authentication import JWTAuth

from account.models import Account, Transaction
from account.schemas import TransactionOut, AccountAmountSchema, TransferSchema, AccountOut
from account.services import emit, absorb, transfer
from user.models import User, Role
from user.utils import check_admin


@api_controller('/', tags=['Account'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class AccountController(ControllerBase):
    @http_post('accounts/emit', response=Optional[TransactionOut])
    def emit(self, payload: AccountAmountSchema):
        check_admin(self.context)

        account = get_object_or_404(Account, id=payload.account_id)
        return emit(account, payload.amount)

    @http_post('accounts/absorb', response=Optional[TransactionOut])
    def absorb(self, payload: AccountAmountSchema):
        check_admin(self.context)

        account = get_object_or_404(Account, id=payload.account_id)
        return absorb(account, payload.amount)

    @http_post('account/transfer', response=TransactionOut)
    def transfer(self, payload: TransferSchema):
        check_admin(self.context)

        account_from = get_object_or_404(Account, id=payload.account_id_from)
        account_to = get_object_or_404(Account, id=payload.account_id_to)
        return transfer(account_from, account_to, payload.amount)

    @http_get('accounts/{account_id}/transactions', response=List[TransactionOut])
    @pagination.paginate
    def get_transactions(self, account_id: int):
        user: User = self.context.request.auth
        if user.team.account_id != account_id:
            check_admin(self.context)

        account = get_object_or_404(Account, id=account_id)
        transactions = Transaction.objects.filter(Q(from_account=account) | Q(to_account=account)).order_by('timestamp')
        return transactions

    @http_get('accounts/{account_id}', response=AccountOut)
    def get_account(self, account_id: int):
        user: User = self.context.request.auth
        if  user.role != Role.MANUFACTURER:
                if user.team.account_id != account_id:
                    check_admin(self.context)

        account = get_object_or_404(Account, id=account_id)
        return account

    @http_get('accounts', response=List[AccountOut])
    @pagination.paginate
    def list_accounts(self):
        check_admin(self.context)

        qs = Account.objects.all()
        return qs
    


@api_controller('/', tags=['Transaction'], permissions=[permissions.IsAuthenticated], auth=JWTAuth())
class TransactionController(ControllerBase):
    @http_get('transactions/{transaction_id}', response=TransactionOut)
    def get_transaction(self, transaction_id: int):
        check_admin(self.context)

        transaction = get_object_or_404(Transaction, id=transaction_id)
        return transaction

    @http_get('transactions', response=List[TransactionOut])
    @pagination.paginate
    def list_transactions(self):
        check_admin(self.context)

        qs = Transaction.objects.all()
        return qs
