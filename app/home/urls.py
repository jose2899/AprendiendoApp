
from django.urls import path

#Views
from app.home.views import index

urlpatterns = [
    path('', index, name='index'),
]
