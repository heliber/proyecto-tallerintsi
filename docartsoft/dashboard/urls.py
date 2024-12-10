from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import generar_reporte_pdf
from .views import bandeja_entrada

app_name = 'dashboard'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('general/', views.general, name='general'),
    path('documentos/', views.documentos, name='documentos'),
    path('crear_documentos', views.crear_documento, name='crear_documento'),
    #path('reporte/', views.reporte, name='reporte'),
    #path('ajustes/', views.ajustes, name='ajustes'),
    path('registro/', views.registro, name='registro'), # registro usuarios
    path('documentos/<int:documento_id>/editar/', views.editar_documento, name='editar_documento'),
    path('documentos/eliminar/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('crear_proyecto', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/eliminar/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('reporte-documentos/', generar_reporte_pdf, name='reporte_documentos'),
    path('bandeja-entrada/', views.bandeja_entrada, name='bandeja_entrada'), #bandeja entrada
    path('detalle/<int:documento_id>/', views.detalle_documento, name='detalle_documento'), # bandeja entrada
    path('nosotros/', views.nosotros, name='nosotros'), # pagina de informacion de nosotros
    path('informacion/', views.informacion, name='informacion'), # pagina de informacion de documentacion
]