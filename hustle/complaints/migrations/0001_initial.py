# Generated by Django 4.0.2 on 2022-02-23 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('no_show', 'Worker did not show up to complete the job.'), ('bad_job', 'Worker did not complete the job satisfactorily.'), ('suspicious', 'Worker was acting suspicious while on or around my property.'), ('other', 'Other')], max_length=100)),
                ('other_reason', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=30)),
            ],
        ),
    ]
