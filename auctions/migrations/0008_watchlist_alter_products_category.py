# Generated by Django 4.1.2 on 2022-12-25 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_comments_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('product', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('Other', 'Other'), ('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Vehicles', 'Vehicles'), ('Technology', 'Technology')], default=('Other', 'Other'), max_length=150),
        ),
    ]
