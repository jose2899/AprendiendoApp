from django.contrib import admin

#models
from app.servicios.models import Servicios
from app.servicios.models import Paquete

# Register your models here.

admin.site.register(Servicios)
admin.site.register(Paquete)