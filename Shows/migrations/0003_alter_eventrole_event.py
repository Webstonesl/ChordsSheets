# Generated by Django 4.2.7 on 2023-11-15 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Shows", "0002_alter_eventrole_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventrole",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Shows.event"
            ),
        ),
    ]
