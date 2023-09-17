from django.apps import AppConfig

class CalendarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.calendario'

    def ready(self):
        import app.calendario.signals  # Importa el archivo de señales cuando la aplicación está lista.
