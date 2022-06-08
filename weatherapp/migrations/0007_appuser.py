# Generated by Django 4.0.4 on 2022-06-07 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weatherapp', '0006_delete_appuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.CharField(max_length=10)),
                ('cities', models.ManyToManyField(to='weatherapp.city')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Application User',
                'verbose_name_plural': 'Application Users',
            },
        ),
    ]