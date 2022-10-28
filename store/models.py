from django.db import models

from product.models import ProductKit, Product
from team.models import Team

# INFO: заменил OneToOneField на ForeignKey
class TeamProductKit(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    product_kit = models.ForeignKey(ProductKit, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

# INFO: заменил OneToOneField на ForeignKey
class TeamProduct(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
