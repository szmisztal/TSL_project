# Generated by Django 4.2.3 on 2023-07-04 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistician_app', '0002_tankertrailer_transportationorder_tanker_trailer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationorder',
            name='load_weight',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24000)]),
        ),
    ]
