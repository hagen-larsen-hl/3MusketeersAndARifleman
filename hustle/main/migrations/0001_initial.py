# Generated by Django 4.0.2 on 2022-03-22 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='customer_data', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('street', models.CharField(max_length=128)),
                ('street2', models.CharField(max_length=16)),
                ('city', models.CharField(max_length=32)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='data', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('phone_number', models.CharField(default='0000000000', max_length=16, unique=True)),
                ('money', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerData',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='worker_data', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]