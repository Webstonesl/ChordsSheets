# Generated by Django 4.2.7 on 2023-11-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Shows", "0003_alter_eventrole_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="start",
            field=models.DateTimeField(),
        ),
    ]