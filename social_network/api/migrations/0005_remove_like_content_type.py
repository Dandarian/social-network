# Generated by Django 3.1 on 2021-04-10 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210410_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='content_type',
        ),
    ]
