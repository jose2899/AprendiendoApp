# myproject/middleware.py

from django.shortcuts import redirect
from django.conf import settings
import re

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info

        # Lista de rutas que no requieren autenticación
        exempt_urls = [settings.LOGIN_URL, '/login/']

        # Verifica si la URL está en la lista de excepciones
        if any(re.match(url, path) for url in exempt_urls):
            return None

        # Si el usuario no está autenticado, redirige a la URL de login
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return None
