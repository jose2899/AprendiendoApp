# Generated by Django 4.2.4 on 2024-01-22 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terapiass', '0008_diagnostico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='nombre_diagnostico',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
