# Generated by Django 3.2.4 on 2023-10-25 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terapiass', '0006_auto_20231025_0735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horarioterapia',
            name='dia_semana',
        ),
        migrations.RemoveField(
            model_name='horarioterapia',
            name='terapia',
        ),
    ]
