# Generated by Django 3.1.2 on 2020-11-07 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20201107_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
