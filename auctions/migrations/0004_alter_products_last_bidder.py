# Generated by Django 4.1.2 on 2022-10-13 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_products_last_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='last_bidder',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
