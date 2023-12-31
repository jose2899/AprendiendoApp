# Generated by Django 3.2.4 on 2023-10-19 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servicios', '0004_paquete'),
        ('psicologo', '0004_rename_psicologos_psicologo'),
        ('usuario', '0002_alter_estudiante_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terapia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicios.paquete')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionPsicologo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=20)),
                ('psicologo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psicologo.psicologo')),
                ('terapia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terapiass.terapia')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionEstudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.estudiante')),
                ('terapia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terapiass.terapia')),
            ],
        ),
    ]
