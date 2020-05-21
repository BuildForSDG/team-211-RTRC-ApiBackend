# Generated by Django 2.2.10 on 2020-05-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]