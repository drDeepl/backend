# Generated by Django 4.1.6 on 2023-07-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamproduct',
            name='count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество'),
        ),
    ]