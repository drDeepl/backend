# Generated by Django 4.0.1 on 2022-10-18 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('store', '0002_teamproduct_timestamp_teamproductkit_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamproduct',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team'),
        ),
        migrations.AlterField(
            model_name='teamproductkit',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team'),
        ),
    ]
