# Generated by Django 4.2.3 on 2024-01-31 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_appusers_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appusers',
            name='adress',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
