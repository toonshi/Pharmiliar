# Generated by Django 5.0.2 on 2024-02-22 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0002_institution_opening_hours_friday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='user_profile',
        ),
    ]
