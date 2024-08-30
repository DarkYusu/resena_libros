from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Agenda, Cita, Especialista, CentroMedico, Perfil
from .forms import AgendaForm, CitaForm, RegistroForm, ContactoForm, TipoUsuarioForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
    
# Vista de inicio
def inicio(request):
    return render(request, 'inicio.html')

# Vista de contacto
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar el formulario de contacto
            return redirect('inicio')
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('agendas')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('agendas')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista de agendas (paginación y filtros)
@login_required
def agendas(request):
    # Obtener los filtros de la solicitud GET
    filtro_centro = request.GET.get('centro_medico')
    filtro_especialista = request.GET.get('especialista')
    filtro_fecha = request.GET.get('fecha')

    # Filtrar las agendas
    agendas_list = Agenda.objects.all()

    if filtro_centro:
        agendas_list = agendas_list.filter(centro_medico_id=filtro_centro)
    if filtro_especialista:
        agendas_list = agendas_list.filter(especialista_id=filtro_especialista)
    if filtro_fecha:
        agendas_list = agendas_list.filter(fecha_disponible=filtro_fecha)

    # Obtener las citas ocupadas
    citas_ocupadas = Cita.objects.filter(agenda__in=agendas_list).values_list('agenda_id', flat=True)

    # Pasar los datos al contexto
    context = {
        'agendas': agendas_list,
        'citas_ocupadas': citas_ocupadas,
        'centros_medicos': CentroMedico.objects.all(),
        'especialistas': Especialista.objects.all(),
    }
    return render(request, 'agendas.html', context)

# Vista para crear una nueva agenda (solo para administradores)
@login_required
def crear_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendas')
    else:
        form = AgendaForm()
    
    especialistas = Especialista.objects.all()
    centros_medicos = CentroMedico.objects.all()

    context = {
        'form': form,
        'especialistas': especialistas,
        'centros_medicos': centros_medicos,
    }
    return render(request, 'crear_agenda.html', context)

@login_required
def detalle_agenda(request, id):
    agenda = get_object_or_404(Agenda, id=id)
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            if Cita.objects.filter(agenda=agenda, usuario=request.user).exists():
                messages.error(request, "Ya tienes una cita en este horario.")
            elif Cita.objects.filter(agenda=agenda).exists():
                messages.error(request, "La hora ya está ocupada por otro usuario.")
            else:
                cita = form.save(commit=False)
                cita.agenda = agenda
                cita.usuario = request.user
                cita.save()
                messages.success(request, "Cita registrada exitosamente.")
                return redirect('agendas')
    else:
        form = CitaForm()

    return render(request, 'detalle_agenda.html', {'agenda': agenda, 'form': form})

@login_required
def seleccionar_tipo_usuario(request):
    if request.method == 'POST':
        form = TipoUsuarioForm(request.POST)
        if form.is_valid():
            tipo_usuario = form.cleaned_data['tipo_usuario']
            perfil, created = Perfil.objects.get_or_create(user=request.user)
            perfil.tipo_usuario = tipo_usuario
            perfil.save()
            return redirect('agendas')  # Cambia 'alguna_otravista' al nombre de la vista que desees
    else:
        form = TipoUsuarioForm()

    return render(request, 'seleccionar_tipo_usuario.html', {'form': form})

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            
            # Enviar correo (asegúrate de configurar el backend de correo en settings.py)
            send_mail(
                subject=f"Nuevo mensaje de {nombre}",
                message=mensaje,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return redirect('contacto_exito')  # Redirige a una página de éxito
    else:
        form = ContactoForm()
    
    return render(request, 'contacto.html', {'form': form})