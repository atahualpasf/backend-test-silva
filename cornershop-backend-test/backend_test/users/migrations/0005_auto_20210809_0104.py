# Generated by Django 3.0.8 on 2021-08-09 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210808_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, help_text='Indicator to know if a object was deleted or not', verbose_name='soft deleted status'),
        ),
    ]
