# Generated by Django 4.0.4 on 2022-06-07 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0005_alter_appuser_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppUser',
        ),
    ]
