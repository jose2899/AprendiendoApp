# Generated by Django 4.2.4 on 2023-09-26 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psicologo', '0003_rename_psicologo_psicologos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Psicologos',
            new_name='Psicologo',
        ),
    ]
