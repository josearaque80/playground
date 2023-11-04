from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
def custom_upload_to(instance, filename):    # Funcion para subir imagenes
    old_instance = Profile.objects.get(pk=instance.pk)   # Obtenemos la instancia anterior
    old_instance.avatar.delete()    # Borramos la imagen anterior
    return 'profiles/' + filename   # Retornamos el nombre de la imagen
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  # Relacion uno a uno
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)    # Imagen
    bio = models.TextField(max_length=500, null=True, blank=True)   # Biografia
    link = models.URLField(max_length=200, null=True, blank=True)   # Enlace

    class Meta:
        ordering = ['user__username']

@receiver(post_save, sender=User)   # Señal que se ejecuta despues de que se guarde un usuario
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):    # Si se ha creado un usuario
        Profile.objects.get_or_create(user=instance)
        # print('Se ha creado un usuario y su perfil asociado')