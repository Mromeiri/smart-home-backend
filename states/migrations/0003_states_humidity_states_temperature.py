# Generated by Django 4.0.5 on 2024-04-03 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0002_states_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='states',
            name='humidity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='states',
            name='temperature',
            field=models.PositiveIntegerField(default=0),
        ),
    ]