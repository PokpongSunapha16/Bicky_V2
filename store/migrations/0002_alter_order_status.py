# Generated by Django 5.1.5 on 2025-03-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'รอดำเนินการ'), ('completed', 'สั่งซื้อสำเร็จ')], default='pending', max_length=10),
        ),
    ]
