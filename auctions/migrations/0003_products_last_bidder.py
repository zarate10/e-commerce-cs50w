# Generated by Django 4.1.2 on 2022-10-12 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_products_category_products_last_offer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='last_bidder',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
