# Generated by Django 3.1.3 on 2020-11-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle_schedule', '0006_auto_20201124_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='battleevent',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
