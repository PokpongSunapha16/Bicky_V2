# Generated by Django 4.2.7 on 2025-03-02 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_orderitem_order_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin')], default='customer', max_length=10),
        ),
    ]
