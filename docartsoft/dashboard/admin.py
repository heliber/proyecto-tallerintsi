from django.contrib import admin
from .models import Documento
#from .models import Proyecto
from .models import Notificacion # bandeja de entrada
# Register your models here.
admin.site.register(Documento)
#admin.site.register(Proyecto)
admin.site.register(Notificacion) # bandeja de entrada