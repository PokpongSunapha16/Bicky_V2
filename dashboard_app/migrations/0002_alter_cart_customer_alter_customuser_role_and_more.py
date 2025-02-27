# Generated by Django 5.1.3 on 2025-02-27 07:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller'), ('admin', 'Admin')], default='customer', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='dashboard_app.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='dashboard_app.order'),
        ),
    ]
