# Generated by Django 4.0.5 on 2024-04-30 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthomeDataSets', '0007_alter_weatherdata_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
