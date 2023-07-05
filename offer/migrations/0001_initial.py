# Generated by Django 4.1.6 on 2023-07-05 06:46

from django.db import migrations, models
import django.db.models.deletion
import offer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[(offer.models.OfferState['DONE'], 'Done'), (offer.models.OfferState['DELETED'], 'Deleted'), (offer.models.OfferState['ACTIVE'], 'Active'), (offer.models.OfferState['AWAIT'], 'Await')], default=offer.models.OfferState['ACTIVE'], max_length=16)),
                ('to_customer', models.IntegerField()),
                ('count', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SaleOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[(offer.models.OfferState['DONE'], 'Done'), (offer.models.OfferState['DELETED'], 'Deleted'), (offer.models.OfferState['ACTIVE'], 'Active'), (offer.models.OfferState['AWAIT'], 'Await')], default=offer.models.OfferState['ACTIVE'], max_length=16)),
                ('product_kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_kit', to='product.productkit')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
