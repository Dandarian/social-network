# Generated by Django 3.1 on 2021-04-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_like_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
