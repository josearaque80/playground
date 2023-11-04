from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView): # ListView: muestra una lista de objetos
    template_name = 'messenger/thread_list.html'

method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView): # DetailView: muestra el detalle de un objeto
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()    # Obtiene el objeto
        if self.request.user not in obj.users.all():    # Si el usuario no está en el hilo
            raise Http404()                            # Lanza un error
        return obj                                    # Si está, devuelve el objeto

def add_message(request, pk):
    json_response = {'created': False}  # Inicializa la respuesta
    if request.user.is_authenticated:  # Si el usuario está autenticado
        content = request.GET.get('content', None)  # Obtiene el contenido del mensaje
        if content:  # Si hay contenido
            thread = get_object_or_404(Thread, pk=pk)  # Obtiene el hilo
            message = Message.objects.create(user=request.user, content=content)  # Crea el mensaje
            thread.messages.add(message)  # Añade el mensaje al hilo
            json_response['created'] = True  # Cambia el valor de la respuesta
            if len(thread.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)  # Devuelve la respuesta en formato JSON

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)  # Obtiene el usuario
    thread = Thread.objects.find_or_create(user, request.user)  # Obtiene el hilo o lo crea
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))  # Redirige al hilo