# Generated by Django 4.0.5 on 2024-03-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthomeDataSets', '0002_alter_lightdataset_dayofweek'),
    ]

    operations = [
        migrations.AddField(
            model_name='lightdataset',
            name='active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
