# Generated by Django 4.2.3 on 2024-01-31 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appusers',
            name='last_login',
        ),
    ]
