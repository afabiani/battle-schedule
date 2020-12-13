# Generated by Django 3.1.3 on 2020-11-25 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle_schedule', '0009_auto_20201125_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battleevent',
            name='type',
            field=models.CharField(choices=[('neutral', 'Neutral'), ('capture', 'Capture'), ('defence', 'Defence'), ('lvl 1 all can capture', 'Lvl 1 All can capture')], default='neutral', max_length=255),
        ),
    ]