# Generated by Django 4.1.2 on 2022-10-15 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.CharField(max_length=150),
        ),
    ]