# Generated by Django 3.1 on 2021-04-12 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_usersactivity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UsersActivity',
            new_name='UserActivity',
        ),
    ]
