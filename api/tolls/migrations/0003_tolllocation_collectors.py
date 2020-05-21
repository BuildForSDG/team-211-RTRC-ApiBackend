# Generated by Django 2.2.10 on 2020-05-12 16:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tolls', '0002_tolllocation_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tolllocation',
            name='collectors',
            field=models.ManyToManyField(related_name='collectors', to=settings.AUTH_USER_MODEL),
        ),
    ]
