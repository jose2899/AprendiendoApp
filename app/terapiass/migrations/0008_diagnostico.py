# Generated by Django 4.2.4 on 2024-01-22 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terapiass', '0007_auto_20231025_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_diagnostico', models.CharField(max_length=255)),
            ],
        ),
    ]
