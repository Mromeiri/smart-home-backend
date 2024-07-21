# Generated by Django 4.2.3 on 2024-01-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_announcement_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='isread',
        ),
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Announcement/'),
        ),
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_notification/'),
        ),
    ]
