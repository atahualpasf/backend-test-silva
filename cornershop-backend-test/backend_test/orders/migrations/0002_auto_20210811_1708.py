# Generated by Django 3.0.8 on 2021-08-11 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0001_initial'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', related_query_name='order', to='users.Employee', verbose_name='employee'),
        ),
        migrations.AddField(
            model_name='order',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', related_query_name='order', to='menus.Meal', verbose_name='meal'),
        ),
        migrations.AddField(
            model_name='order',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', related_query_name='order', to='menus.Menu', verbose_name='menu'),
        ),
    ]
