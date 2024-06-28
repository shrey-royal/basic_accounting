# Generated by Django 3.2.10 on 2024-06-05 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20240605_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selected',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_no', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(blank=True, max_length=20, null=True)),
                ('packing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.packing')),
            ],
        ),
    ]
