from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .models import Documento, Proyecto
from .forms import DocumentoForm, RegistroForm, ProyectoForm
#from django.views.generic import TemplateView
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#class HomePageView(TemplateView):
    #template_name = "inicio.html"  # Asegúrate de que esta plantilla exista

def inicio(request):
    return render(request, 'inicio.html')

#def registro(request):
    #return render(request, 'registro.html')
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda al usuario en la base de datos
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            #return redirect('login')  # Redirige al inicio de sesión
            return redirect('inicio')  # Redirige al inicio de sesión
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def general(request):
    proyectos_recientes = Proyecto.objects.filter(usuario=request.user).order_by('-fecha_creacion')[:4]
    context = {
        'nombre_usuario': request.user.first_name or request.user.username,
        'proyectos_recientes': proyectos_recientes,
        #'fecha_actual': timezone.now()
    }
    return render(request, 'general.html', context)

@login_required
def documentos(request):
    documentos_recientes = Documento.objects.filter(creado_por=request.user).order_by('-fecha_creacion')
    documentos_compartidos = Documento.objects.filter(compartido_con=request.user)
    context = {
        'nombre_usuario': request.user.first_name or request.user.username,
        'documentos_recientes': documentos_recientes,
        'documentos_compartidos': documentos_compartidos
    }
    return render(request, 'documentos.html', context)
    #documentos = []  # Reemplaza con tu consulta, por ejemplo: ModeloDocumento.objects.all()
    #return render(request, 'documentos.html', {'documentos': documentos})

@login_required
def crear_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.creado_por = request.user
            documento.save()
            return redirect('dashboard:documentos')
    else:
        form = DocumentoForm()
    return render(request, 'crear_documento.html', {'form': form})

# codigo para editar documento y eliminar documento

@login_required
def editar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id, creado_por=request.user)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento actualizado exitosamente.')
            return redirect('dashboard:documentos')
    else:
        form = DocumentoForm(instance=documento)
    
    return render(request, 'editar_documento.html', {'form': form, 'documento': documento})

@login_required
def eliminar_documento(request, documento_id):
    if request.method == 'POST':
        documento = get_object_or_404(Documento, id=documento_id, creado_por=request.user)
        documento.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)  # Method Not Allowed

# codigo para proyecto, detalle proyecto y eliminar proyecto
@login_required
def proyectos(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    return render(request, 'proyectos.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            #proyecto.creado_por = request.user
            proyecto.usuario = request.user  # Asigna el usuario autenticado
            proyecto.save()
            #proyecto.miembros.add(request.user)
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('dashboard:proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})

@login_required
#def detalle_proyecto(request, proyecto_id):
#    proyecto = get_object_or_404(Proyecto, id=proyecto_id, usuario=request.user)
#    documentos = proyecto.documentos.all()
#    return render(request, 'detalle_proyecto.html', {'proyecto': proyecto, 'documentos': documentos})
def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, usuario=request.user)
    documentos = proyecto.documentos.all()  # Cambiar si el related_name es distinto
    return render(request, 'dashboard/detalle_proyecto.html', {
        'proyecto': proyecto,
        'documentos': documentos,
    })

@login_required
def eliminar_proyecto(request, proyecto_id):
    if request.method == 'POST':
        proyecto = get_object_or_404(Proyecto, id=proyecto_id, creado_por=request.user)
        proyecto.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)

@login_required
def generar_reporte_pdf(request):
    documentos = Documento.objects.all() # Puedes aplicar filtros según tu necesidad  # Optimiza la consulta con select_related
    template_path = 'reporte_documentos.html'
    context = {
        'documentos': documentos,
        #'nombre_usuario': request.user.first_name or request.user.username,
        }

    # Renderizar la plantilla como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_documentos.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response