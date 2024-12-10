from django.db import models
from django.contrib.auth.models import User
#from .models import Proyecto

#para el Documento
class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_vista = models.DateTimeField(null=True, blank=True)
    etiquetas = models.CharField(max_length=200, blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    compartido_con = models.ManyToManyField(User, related_name='documentos_compartidos', blank=True)
    #proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='documentos')
   
    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
# para el proyecto

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    

    def __str__(self):
        return self.nombre
    
# bandeja de entrada 
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    documento = models.ForeignKey('Documento', on_delete=models.CASCADE, null=True, blank=True)  # Relación con documento editado
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notificación para {self.usuario.username}'