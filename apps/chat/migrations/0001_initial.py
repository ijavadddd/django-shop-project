# Generated by Django 4.1.6 on 2023-02-10 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=800, verbose_name='متن')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='زمان انتشار')),
                ('object_id', models.PositiveIntegerField(verbose_name='آیدی رکورد مدل')),
                ('approved', models.BooleanField(default=False, help_text='در صورتی که کامنت تایید شده باشد، نشان داده خواهد شد', verbose_name='تایید شده')),
                ('content_type', models.ForeignKey(help_text='کامنت مربوط به کدام مدل است', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='مدل')),
                ('reply_to', models.ForeignKey(blank=True, help_text='در صورتی که کامنت پاسخ کامنت دیگری باشد این قسمت پر میشود', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='chat.comment', verbose_name='پاسخ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت\u200cها',
            },
        ),
    ]