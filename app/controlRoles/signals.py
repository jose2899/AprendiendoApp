from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.usuarios.usuario.models import Estudiante, Representante
from app.usuarios.psicologo.models import Psicologo
from app.usuarios.adminis.models import Adminis
from app.servicios.models import Paquete

def create_groups_and_permissions(sender, **kwargs):
    # Crear grupo de psicólogos
    psicologo_group, created = Group.objects.get_or_create(name='Psicologos')

    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    # Definir permisos específicos para el modelo Psicologo
    content_type_psicologo = ContentType.objects.get_for_model(Psicologo)
    
    content_type_adminis = ContentType.objects.get_for_model(Adminis)


    permiso_create_psicologo, created = Permission.objects.get_or_create(
        codename='can_create_psicologo',
        name='Can create Psicologo',
        content_type=content_type_psicologo,
    )

    permiso_create_adminis, _ = Permission.objects.get_or_create(
        codename='can_create_adminis',
        name='Can create Adminis',
        content_type=content_type_adminis,
    )

    # Asignar permisos a los administradores, pero no a los psicólogos
    psicologo_group.permissions.add()
    
    # Asignar todos los permisos al grupo Administradores
    admin_group.permissions.add(permiso_create_adminis)

# Conectar la señal
post_migrate.connect(create_groups_and_permissions)