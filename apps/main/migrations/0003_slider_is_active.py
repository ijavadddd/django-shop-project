# Generated by Django 4.2.3 on 2023-07-17 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_brand_alter_slider_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
    ]