# Generated by Django 3.2.10 on 2024-05-25 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_lottdata_lot_no_alter_lott_lot_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('bill_no', models.CharField(max_length=20)),
                ('date', models.DateTimeField(max_length=20)),
            ],
        ),
    ]
