from django.contrib import admin

# Register your models here.
from app.bitacora.models import Bitacora, NuevaBitacora

admin.site.register(Bitacora)
admin.site.register(NuevaBitacora)
