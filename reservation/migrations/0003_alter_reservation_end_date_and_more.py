# Generated by Django 5.0 on 2024-01-08   23:20


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_servicereservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
