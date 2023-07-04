# Generated by Django 4.2.3 on 2023-07-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistician_app', '0003_alter_transportationorder_load_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationorder',
            name='trailer_type',
            field=models.CharField(choices=[('Curtain-side trailer', 'Curtain Side'), ('Refrigerated trailer', 'Refrigerated'), ('Tipper trailer', 'Tipper'), ('Low-loader trailer', 'Low Loader'), ('Container trailer', 'Container'), ('Tanker trailer', 'Tanker'), ('Self-unloading trailer', 'Self Unloading'), ('Insulated trailer', 'Insulated')], max_length=64),
        ),
    ]
