# Generated by Django 5.2.1 on 2025-06-02 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trainings", "0003_alter_group_price_schedule"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Schedule",
        ),
    ]
