# Generated by Django 4.2.3 on 2023-07-03 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logistician_app', '0003_remove_delivery_transportation_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportationorder',
            name='delivery',
        ),
        migrations.AddField(
            model_name='delivery',
            name='transportation_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to='logistician_app.transportationorder'),
            preserve_default=False,
        ),
    ]
