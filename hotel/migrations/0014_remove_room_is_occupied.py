# Generated by Django 5.0 on 2024-01-07   03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0013_room_is_occupied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_occupied',
        ),
    ]
