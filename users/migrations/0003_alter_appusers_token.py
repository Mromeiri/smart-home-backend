# Generated by Django 4.2.3 on 2024-01-31 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_appusers_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appusers',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]