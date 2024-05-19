from django.test import TestCase
from django.urls import reverse
from app.usuarios.usuario.models import Representante, Estudiante
from app.planificaciones.models import Planificacion
from app.terapiass.models import Diagnostico
from app.bitacora.models import Bitacora, NuevaBitacora

class BitacoraTest(TestCase):
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
        self.estudiante = Estudiante.objects.create(
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
        self.diagnostico = Diagnostico.objects.create(
            nombre_diagnostico='TDAH',
        )

        # Crear una planificación para el estudiante con el diagnóstico
        self.planificacion = Planificacion.objects.create(
            estudiante=self.estudiante,
            diagnostico=self.diagnostico,
            edad_biologica=10,
            edad_cognitiva_lenguaje_verbal=8,
            edad_cognitiva_lenguaje_comprensivo=7
        )

        # Crear una bitácora para la planificación
        self.bitacora = Bitacora.objects.create(
            estudiante=self.estudiante,
            planificacion=self.planificacion,
            diagnostico=self.diagnostico
        )

        # Crear una nueva bitácora para la bitácora creada anteriormente
        self.nueva_bitacora = NuevaBitacora.objects.create(
            bitacora=self.bitacora,
            fecha='2024-03-10',
            observacion_conducta='buena',
            temas_trabajados='Tema 1, Tema 2',
            avance='regular',
            firma_terapeuta='Firma Terapeuta',
            revisado_por='Supervisor',
            asistencias='si'
        )

    def test_creacion_estudiante_representante(self):
        representante = Representante.objects.get(nombre='Juan')
        self.assertEqual(representante.nombre, 'Juan')

        estudiante = Estudiante.objects.get(nombre='John')
        self.assertEqual(estudiante.nombre, 'John')

    def test_creacion_planificacion(self):
        planificacion = Planificacion.objects.get(estudiante=self.estudiante)
        self.assertEqual(planificacion.diagnostico.nombre_diagnostico, 'TDAH')

    def test_creacion_bitacora(self):
        bitacora = Bitacora.objects.get(estudiante=self.estudiante)
        self.assertEqual(bitacora.planificacion, self.planificacion)

    def test_creacion_nueva_bitacora(self):
        nueva_bitacora = NuevaBitacora.objects.get(bitacora=self.bitacora)
        self.assertEqual(nueva_bitacora.observacion_conducta, 'buena')

    def test_listar_bitacoras(self):
            response = self.client.get(reverse('listar_bitacora'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'bitacora')

    def test_visualizar_bitacora(self):
        response = self.client.get(reverse('ver_bitacora', kwargs={'pk': self.bitacora.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bitacora')