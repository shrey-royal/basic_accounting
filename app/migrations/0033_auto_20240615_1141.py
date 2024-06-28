# Generated by Django 3.2.10 on 2024-06-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20240615_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='packing_slip_new',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_no', models.CharField(blank=True, max_length=20, null=True)),
                ('vehicle_no', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='bundle',
            old_name='packing',
            new_name='bundle_entry',
        ),
        migrations.AlterField(
            model_name='packing',
            name='date_packing',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='selected',
            name='date',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='PackingSlipNew',
        ),
    ]
