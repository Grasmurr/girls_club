# Generated by Django 4.2.7 on 2023-11-18 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("serviceapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="event_date",
            field=models.DateField(null=True),
        ),
    ]
