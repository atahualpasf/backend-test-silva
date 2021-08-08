# Generated by Django 3.0.8 on 2021-08-07 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='slack_username',
            field=models.CharField(error_messages={'unique': 'A employee with that slack username already exists.'}, max_length=50, unique=True, verbose_name='slack username'),
        ),
    ]