# Generated by Django 4.2.6 on 2024-04-01 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="borrowedbook",
            name="user",
        ),
    ]
