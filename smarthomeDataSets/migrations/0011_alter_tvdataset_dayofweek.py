# Generated by Django 4.0.5 on 2024-05-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthomeDataSets', '0010_tvdataset_motiondetection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvdataset',
            name='dayOfWeek',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
