# Generated by Django 4.2.7 on 2023-11-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Music", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chordsheetroles",
            name="lastupdate",
            field=models.DateTimeField(auto_now=True),
        ),
    ]