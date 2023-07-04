# Generated by Django 4.2.3 on 2023-07-04 10:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistician_app', '0004_alter_transportationorder_trailer_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportationorder',
            name='tanker_trailer',
        ),
        migrations.AlterField(
            model_name='transportationorder',
            name='load_weight',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24000)]),
        ),
    ]