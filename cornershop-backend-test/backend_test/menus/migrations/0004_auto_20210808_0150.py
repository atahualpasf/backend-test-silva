# Generated by Django 3.0.8 on 2021-08-08 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_menuoption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified'], 'verbose_name': 'meal', 'verbose_name_plural': 'meals'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-modified'], 'verbose_name': 'menu', 'verbose_name_plural': 'menus'},
        ),
        migrations.AlterModelOptions(
            name='menuoption',
            options={'get_latest_by': 'created', 'ordering': ['option', '-created'], 'verbose_name': 'menu option', 'verbose_name_plural': 'menu options'},
        ),
    ]