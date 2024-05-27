from django.apps import AppConfig

class ControlrolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.controlRoles'
    
    def ready(self):
        from . import signals