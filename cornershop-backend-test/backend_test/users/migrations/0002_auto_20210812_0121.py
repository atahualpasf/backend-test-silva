# Generated by Django 3.0.8 on 2021-08-12 01:21

import backend_test.users.models.users
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', backend_test.users.models.users.UserManager()),
            ],
        ),
    ]