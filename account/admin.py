from django.contrib import admin

from account.models import Account, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
