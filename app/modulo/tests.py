from django.urls import reverse
from django.test import TestCase, Client
from django_dynamic_fixture import G
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion
from app.bitacora.models import NuevaBitacora

class ModuloViewsTestCase(TestCase):
    def setUp(self):
        # Crear datos de prueba
        self.estudiante = G(Estudiante)
        self.diagnostico = G(Diagnostico, nombre_diagnostico='TDAH')
        self.planificacion = G(Planificacion, estudiante=self.estudiante, diagnostico=self.diagnostico)
        self.bitacora = G(NuevaBitacora, bitacora__estudiante=self.estudiante)
        self.client = Client()  

    def test_seleccionar_estudiante_view(self):
        url = reverse('listar_estudiantes_tdah')  
        response = self.client.get(url)  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modulo/fases_proceso.html')

    def test_transformar_datosF_view(self):
        url = reverse('transformar_datosF', kwargs={'estudiante_id': self.estudiante.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modulo/fases_proceso.html')

    
    def test_cargar_modelo_view(self):
        # Prueba para la vista que carga el modelo
        url = reverse('cargar_modelo', kwargs={'estudiante_id': self.estudiante.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modulo/fases_proceso.html')

    
    #def test_cargar_modelo_view(self):
        # Prueba para la vista que carga el modelo
    #    url = reverse('cargar_modelo', kwargs={'estudiante_id': self.estudiante.pk})
    #    response = self.client.get(url)
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTemplateUsed(response, 'modulo/fases_proceso.html')

        # Verificar si se carga correctamente un modelo
    #    form_data = {
    #        'modelo_pkl': open('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl', 'rb')  # Ruta al modelo a cargar
    #    }
    #   response = self.client.post(url, form_data, format='multipart')
    #    self.assertEqual(response.status_code, 200)
        # Verificar que el mensaje de confirmación está presente en la respuesta
    #    self.assertContains(response, "El modelo se ha cargado correctamente.")

    def test_realizar_prediccion_view(self):
        url = reverse('realizar_prediccion', kwargs={'estudiante_id': self.estudiante.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
