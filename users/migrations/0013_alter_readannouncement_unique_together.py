# Generated by Django 4.2.3 on 2024-01-31 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_readannouncement_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='readannouncement',
            unique_together=set(),
        ),
    ]
