# Generated by Django 2.2.10 on 2020-05-13 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicles', '0002_auto_20200512_1234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VehicleType',
            new_name='VehicleCategory',
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('license_number', models.CharField(max_length=250)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('model', models.CharField(max_length=250)),
                ('chassis_number', models.CharField(max_length=250, unique=True)),
                ('qr_code', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicle_categories', to='vehicles.VehicleCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]