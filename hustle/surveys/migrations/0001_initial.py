# Generated by Django 4.0.2 on 2022-04-13 07:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0006_alter_job_time_estimate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_notes', models.TextField(verbose_name='Duration Notes')),
                ('duration_rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)], verbose_name='Duration Rating')),
                ('complexity_rating', models.IntegerField(verbose_name='Difficulty Rating')),
                ('complexity_notes', models.TextField(verbose_name='Was the job more or less difficult than the customer anticipated?')),
                ('notes', models.TextField(verbose_name='What else should other workers know about this customer?')),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='jobs.job')),
            ],
        ),
    ]
