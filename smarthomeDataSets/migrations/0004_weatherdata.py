# Generated by Django 4.0.5 on 2024-04-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthomeDataSets', '0003_lightdataset_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('day', models.DateField()),
                ('month', models.CharField(max_length=20)),
                ('outside_temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('room_temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('outside_humidity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('room_humidity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('outside_luminosity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('person_count', models.PositiveIntegerField()),
            ],
        ),
    ]
