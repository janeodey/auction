# Generated by Django 3.1.2 on 2020-11-02 16:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20201102_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(help_text='<p>Bid should not be less than current bid.</p>', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
