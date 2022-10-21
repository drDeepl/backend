from django.contrib import admin

from offer.models import SaleOffer, PurchaseOffer, SaleDone, PurchaseDone

admin.site.register(SaleOffer)
admin.site.register(PurchaseOffer)
admin.site.register(SaleDone)
admin.site.register(PurchaseDone)
