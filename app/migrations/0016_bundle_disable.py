# Generated by Django 3.2.10 on 2024-06-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20240605_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundle',
            name='disable',
            field=models.BooleanField(default=False),
        ),
    ]
