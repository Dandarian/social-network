# Generated by Django 3.1 on 2021-04-12 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210412_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='last_request',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]