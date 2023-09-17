from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from app.calendario.models import Evento
from app.calendario.forms import EventoForm
from django.urls import reverse_lazy

# Create your views here.

class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'calendario/crearEvento.html'
    success_url = reverse_lazy('lista_eventos')

class EventoUpdateView(UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'calendario/editarEvento.html'
    success_url = reverse_lazy('lista_eventos')

class EventoListView(ListView):
    model = Evento
    template_name = 'calendario/listaEvento.html'
    context_object_name = 'eventos'

class EventoDeleteView(DeleteView):
    model = Evento
    template_name = 'calendario/eliminarEvento.html'
    success_url = reverse_lazy('lista_eventos')

def ver_calendario(request):
    eventos = Evento.objects.all()  # Obtén la lista de eventos desde la base de datos
    return render(request, 'calendario/calendario.html', {'eventos': eventos})

def obtener_eventos(request):
    eventos = Evento.objects.all()
    data = []
    for evento in eventos:
        data.append({
            'title': evento.titulo,
            'start': evento.fecha_registro.isoformat(),
            'end': evento.fecha_termino.isoformat(),
            'description': evento.observacion,
        })
    return JsonResponse(data, safe=False)