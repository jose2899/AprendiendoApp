from django.test import TestCase
from app.usuarios.usuario.models import Representante, Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion, PlanificacionSemana

class CrearPlanificacionTestCase(TestCase):
    def setUp(self):
        # Crear un representante
        representante = Representante.objects.create(
            nombre='Juan',
            apellido='Pérez',
            telefono='1234567',
            celular='987654321',
            email='juan@example.com',
            cedula='1234567890',
            servicios='Terapia de Lenguaje',
            otra_terapia='Otra terapia',
            conocido='Conocido',
            observacion='Observación'
        )

        # Crear un estudiante asociado al representante
        estudiante = Estudiante.objects.create(
            representante=representante,
            nombre='John',
            apellido='Doe',
            genero='Masculino',
            cedula='1234567890',
            fecha_nacimiento='2005-01-01',
            fecha='2022-01-01',
            edad=10,
            año_educacion=5,
            institucion_educativa='Escuela Primaria',
            motivo='Motivo'
        )

        # Crear un diagnóstico asociado a la planificación
        diagnostico = Diagnostico.objects.create(
            nombre_diagnostico='TDAH',
        )

        # Crear una planificación para el estudiante con el diagnóstico
        planificacion = Planificacion.objects.create(
            estudiante=estudiante,
            diagnostico=diagnostico,
            edad_biologica=10,
            edad_cognitiva_lenguaje_verbal=8,
            edad_cognitiva_lenguaje_comprensivo=7
        )

        # Crear una planificación semanal asociada a la planificación
        self.planificacion_semana = PlanificacionSemana.objects.create(
            planificacion=planificacion,
            numero_semana=1,
            tiempo_previsto='5 horas',
            objetivo='Objetivo de la semana',
            actividad_lenguaje='Actividad de lenguaje',
            actividad_cognitiva='Actividad cognitiva',
            actividad_sensorial='Actividad sensorial',
            actividades_internalizadas='Actividades internalizadas',
            actividades_reforzar='Actividades a reforzar'
        )

    def test_creacion_planificacion(self):
        # Verificar si la planificación se creó correctamente
        planificacion = Planificacion.objects.get(estudiante__nombre='John')
        self.assertEqual(planificacion.estudiante.nombre, 'John')

    def test_creacion_planificacion_semana(self):
        # Verificar si la planificación semanal se creó correctamente
        planificacion_semana = PlanificacionSemana.objects.get(planificacion__estudiante__nombre='John')
        self.assertEqual(planificacion_semana.numero_semana, 1)

    def test_edicion_planificacion_semana(self):
        # Editar la planificación semanal
        nuevo_objetivo = 'Nuevo objetivo de la semana'
        self.planificacion_semana.objetivo = nuevo_objetivo
        self.planificacion_semana.save()

        # Verificar si la edición se realizó correctamente
        planificacion_semana_editada = PlanificacionSemana.objects.get(planificacion__estudiante__nombre='John')
        self.assertEqual(planificacion_semana_editada.objetivo, nuevo_objetivo)

    def test_eliminacion_planificacion_semana(self):
        # Eliminar la planificación semanal
        self.planificacion_semana.delete()

        # Verificar si la eliminación se realizó correctamente
        with self.assertRaises(PlanificacionSemana.DoesNotExist):
            PlanificacionSemana.objects.get(planificacion__estudiante__nombre='John')
    
