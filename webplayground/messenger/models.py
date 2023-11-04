from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

class ThreadManager(models.Manager):   # creamos un manager para el hilo
    def find(self, user1, user2):  # funcion para buscar el hilo
        queryset = self.filter(users=user1).filter(users=user2) # buscamos el hilo
        if len(queryset) > 0:   # si existe
            return queryset[0]  # retornamos el hilo
        return None # si no existe retornamos None

    def find_or_create(self, user1, user2): # funcion para buscar o crear el hilo
        thread = self.find(user1, user2)    # buscamos el hilo
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread
class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)   # fecha de actualizacion
    objects = ThreadManager()   # agregamos el manager al modelo

    class Meta:
        ordering = ['-updated']    # ordenamos por fecha de actualizacion

def messages_changed(sender, **kwargs): # funcion para que cuando se agregue un mensaje al hilo, se guarde
    instance = kwargs.pop('instance', None) # obtenemos la instancia
    action = kwargs.pop('action', None) # obtenemos la accion
    pk_set = kwargs.pop('pk_set', None) # obtenemos el pk del mensaje
    print(instance, action, pk_set) # imprimimos los valores

    false_pk_set = set()    # creamos un set vacio
    if action is "pre_add": # si la accion es agregar
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all(): # si el usuario no esta en el hilo
                print('Ups! ({}) no forma parte del hilo'.format(msg.user.username)) # imprimimos un mensaje
                false_pk_set.add(msg_pk)    # agregamos el mensaje al set
    # Buscamos los mensajes que no estan en el hilo y los eliminamos del set
    pk_set.difference_update(false_pk_set) # eliminamos los mensajes del set

    instance.save() # guardamos la instancia

m2m_changed.connect(messages_changed, sender=Thread.messages.through)   # conectamos la funcion con el hilo

