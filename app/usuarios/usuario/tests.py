from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.usuarios.usuario.models import Representante, Estudiante

class CrearRepresentanteViewTestCase(TestCase):
    def test_creacion_representante(self):
        # Crear un usuario representante para las pruebas
        representante_data = {
            'nombre': 'John',
            'apellido': 'Doe',
            'telefono': '1234567',
            'celular': '987654321',
            'email': 'john.doe@example.com',
            'cedula': '1234567890',
            'servicios': 'Terapia de Lenguaje',
            'otra_terapia': 'Otra terapia',
            'conocido': 'Conocido',
            'observacion': 'Observacion',
        }
        response = self.client.post(reverse('crear_representante'), representante_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Representante.objects.filter(nombre='John').exists())

class CrearEstudianteViewTestCase(TestCase):
    def setUp(self):
        # Crear un usuario representante para asociarlo al estudiante
        self.representante = Representante.objects.create(nombre='Jane', apellido='Doe', telefono='1234567',
                                                          celular='987654321', email='jane.doe@example.com',
                                                          cedula='1234567890', servicios='Terapia de Lenguaje',
                                                          otra_terapia='Otra terapia', conocido='Conocido',
                                                          observacion='Observacion')

    def test_creacion_estudiante(self):
        # Crear un estudiante asociado al representante creado en setUp
        estudiante_data = {
            'representante': self.representante.id,
            'nombre': 'Alice',
            'apellido': 'Doe',
            'genero': 'Femenino',
            'cedula': '0987654321',
            'fecha_nacimiento': '2005-01-01',
            'edad': 10,
            'año_educacion': 5,
            'institucion_educativa': 'Escuela Primaria',
            'fecha': '2022-01-01',
            'motivo': 'Motivo',
        }
        response = self.client.post(reverse('crear_estudiante'), estudiante_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Estudiante.objects.filter(nombre='Alice').exists())
