# Generated by Django 5.0 on 2024-01-06 11:37


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=500)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
