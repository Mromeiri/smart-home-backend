# Generated by Django 4.0.5 on 2024-05-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0009_states_channelon_states_fanlevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='states',
            name='channelName',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
