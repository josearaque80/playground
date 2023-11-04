from django.urls import path
from .views import ThreadList, ThreadDetail, add_message, start_thread

messenger_patterns = ([
    path('', ThreadList.as_view(), name="list"), # Lista de hilos
    path('thread/<int:pk>/', ThreadDetail.as_view(), name="detail"), # Detalle de un hilo
    path('thread/<int:pk>/add/', add_message, name="add"), # Añadir un mensaje a un hilo
    path('thread/start/<username>/', start_thread, name="start"), # Crear un hilo
], 'messenger') # messenger:namespace