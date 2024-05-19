from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from app.usuarios.adminis.models import Adminis

class AdminisViewsTestCase(TestCase):
    def setUp(self):
        # Crear un usuario administrador para las pruebas
        self.admin_user = User.objects.create_superuser(username='admin1', password='adminpassword', email='admin@example.com')
        self.adminis = Adminis.objects.create(user=self.admin_user, nombre='Admin1', apellido='User', email='admin@example.com')

    def test_listar_admin_view(self):
        # Simular inicio de sesión del usuario administrador
        self.client.login(username='admin1', password='adminpassword')
        response = self.client.get(reverse('listar_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/listarAdmin.html')
        self.assertIn(self.adminis, response.context['objects'])

    def test_crear_admin_view(self):
        self.client.login(username='admin1', password='adminpassword')
        response = self.client.get(reverse('crear_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/crearAdmin.html')

        # Datos del nuevo administrador a crear
        new_admin_data = {
            'username': 'newadmin',
            'password': 'newadminpassword',
            'email': 'newadmin@example.com',
            'nombre': 'Nuevo',
            'apellido': 'Admin1',
            'celular': '1234567890',
            'direccion': 'Calle 123',
        }

        response = self.client.post(reverse('crear_admin'), data=new_admin_data)

        self.assertRedirects(response, reverse('index'))

        self.assertTrue(User.objects.filter(username='newadmin').exists())
        self.assertTrue(Adminis.objects.filter(user__username='newadmin').exists())

    def test_editar_admin_view(self):
        # Simular inicio de sesión del usuario administrador
        self.client.login(username='admin1', password='adminpassword')
        response = self.client.get(reverse('editar_admin', kwargs={'pk': self.adminis.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'usuarios/editarAdmin.html')

    def test_ver_admin_view(self):
        # Simular inicio de sesión del usuario administrador
        self.client.login(username='admin1', password='adminpassword')
        response = self.client.get(reverse('ver_admin', kwargs={'pk': self.adminis.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/verAdmin.html')
        self.assertEqual(self.adminis, response.context['objects'])

    def test_eliminar_admin_view(self):
        # Simular inicio de sesión del usuario administrador
        self.client.login(username='admin1', password='adminpassword')
        response = self.client.get(reverse('eliminar_admin', kwargs={'pk': self.adminis.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/eliminarAdmin.html')

        response = self.client.post(reverse('eliminar_admin', kwargs={'pk': self.adminis.pk}))
        # Verificar que se redirige a la página de listar administradores después de eliminarlo
        self.assertRedirects(response, reverse('listar_admin'))

