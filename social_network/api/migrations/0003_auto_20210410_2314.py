# Generated by Django 3.1 on 2021-04-10 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('api', '0002_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.PositiveIntegerField(),
        ),
    ]
