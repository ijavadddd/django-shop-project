# Generated by Django 4.1.6 on 2023-02-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_by',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=90301065, max_length=8, unique=True, verbose_name='شماره سفارش'),
        ),
        migrations.AlterField(
            model_name='returnorder',
            name='return_order_id',
            field=models.CharField(default=76680042, max_length=8, unique=True, verbose_name='شماره سفارش مرجوعی'),
        ),
    ]