# Generated by Django 3.2.10 on 2024-06-06 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_packing_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packing',
            name='status',
        ),
    ]
