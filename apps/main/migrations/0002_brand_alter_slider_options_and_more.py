# Generated by Django 4.2.3 on 2023-07-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='files/', verbose_name='عکس اسلایدر')),
                ('alt', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برندها',
            },
        ),
        migrations.AlterModelOptions(
            name='slider',
            options={'verbose_name': 'اسلایدر', 'verbose_name_plural': 'اسلایدرها'},
        ),
        migrations.AlterField(
            model_name='slider',
            name='button_action',
            field=models.CharField(blank=True, help_text='یا لینکم ستقسم خارجی یا به صورت \u200c{% "urls "Address %}', max_length=300, null=True, verbose_name='لینک دکمه'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(blank=True, max_length=130, null=True, verbose_name='عنوان'),
        ),
    ]
