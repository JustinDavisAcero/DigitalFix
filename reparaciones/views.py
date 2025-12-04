from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

from .models import Cliente, CitaDiagnostico, RetiroEntrega, Dispositivo, Mensaje, DiagnosticoTecnico, Inventario
from .forms import (
    ClienteForm, RetiroEntregaForm, CitaDiagnosticoForm, MensajeForm,
    DiagnosticoTecnicoForm, InventarioForm
)

def inicio(request):
    return render(request, 'index.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nombre = request.POST.get('nombre') or username
        telefono = request.POST.get('telefono') or ''
        direccion = request.POST.get('direccion') or ''

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registrarse')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('registrarse')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('registrarse')

        user = User.objects.create_user(username=username, email=email, password=password1)
        Cliente.objects.create(user=user, nombre=nombre, correo=email, telefono=telefono, direccion=direccion)
        messages.success(request, 'Cuenta creada correctamente. Ya puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'registro.html')

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                u = User.objects.get(email=username_or_email)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('perfil_cliente')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('index')

@login_required
def perfil_cliente(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'No se encontró perfil de cliente relacionado con tu usuario.')
        return redirect('index')

    dispositivos = Dispositivo.objects.filter(cliente=cliente)
    retiros = RetiroEntrega.objects.filter(cliente=cliente).order_by('-fecha_solicitud')
    citas = CitaDiagnostico.objects.filter(cliente=cliente).order_by('-fecha_hora')
    mensajes = Mensaje.objects.filter(cliente=cliente).order_by('-fecha_envio')

    context = {
        'cliente': cliente,
        'dispositivos': dispositivos,
        'retiros': retiros,
        'citas': citas,
        'mensajes': mensajes
    }
    return render(request, 'cliente.html', context)

@login_required
def dashboard(request):
    citas = CitaDiagnostico.objects.all().order_by('fecha_hora')
    return render(request, 'dashboard.html', {'citas': citas})

@login_required
def agendar_cita(request):
    if request.method == 'POST':
        form = CitaDiagnosticoForm(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                messages.error(request, 'No se encontró perfil de cliente para este usuario.')
                return redirect('agendar_cita')
            cita = form.save(commit=False)
            cita.cliente = cliente
            cita.save()
            messages.success(request, 'Tu cita ha sido agendada correctamente.')
            return redirect('perfil_cliente')
        else:
            messages.error(request, 'Error al agendar la cita. Revisa los datos.')
    else:
        form = CitaDiagnosticoForm()
    return render(request, 'agendar_cita.html', {'form': form})

def estado_reparacion(request):
    estado = None
    orden = None
    if request.method == 'POST':
        orden = request.POST.get('orden')
        if orden:
            dispositivo = Dispositivo.objects.filter(numero_orden=orden).first()
            if dispositivo:
                estado = dispositivo.get_estado_display()
            else:
                messages.warning(request, 'No se encontró la orden indicada.')
        else:
            correo = request.POST.get('correo')
            if correo:
                cliente = Cliente.objects.filter(correo=correo).first()
                if cliente:
                    dispositivo = Dispositivo.objects.filter(cliente=cliente).last()
                    if dispositivo:
                        estado = dispositivo.get_estado_display()
                        orden = dispositivo.numero_orden
                    else:
                        messages.warning(request, 'No hay reparaciones registradas para este cliente.')
                else:
                    messages.error(request, 'Cliente no encontrado.')
    return render(request, 'estado_reparacion.html', {'estado': estado, 'orden': orden})

@login_required
def retiro_entrega(request):
    if request.method == 'POST':
        form = RetiroEntregaForm(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                messages.error(request, 'No se encontró perfil de cliente para este usuario.')
                return redirect('retiro_entrega')
            retiro = form.save(commit=False)
            retiro.cliente = cliente
            retiro.save()
            messages.success(request, f'Solicitud registrada correctamente. N° de orden: {retiro.numero_orden}')
            return redirect('perfil_cliente')
        else:
            messages.error(request, 'Error en el formulario.')
    else:
        form = RetiroEntregaForm()
    return render(request, 'retiro_entrega.html', {'form': form})

@login_required
def mensajes(request):
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                messages.error(request, 'No se encontró perfil de cliente para este usuario.')
                return redirect('mensajes')
            mensaje = form.save(commit=False)
            mensaje.cliente = cliente
            mensaje.save()
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('perfil_cliente')
        else:
            messages.error(request, 'Error en el mensaje.')
    else:
        form = MensajeForm()
    return render(request, 'mensajes.html', {'form': form})

@login_required
def registrar_diagnostico(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)

    if request.method == 'POST':
        form = DiagnosticoTecnicoForm(request.POST)
        if form.is_valid():
            diag = form.save(commit=False)
            diag.dispositivo = dispositivo
            diag.save()
            messages.success(request, "Diagnóstico registrado correctamente.")
            return redirect('dashboard')
        else:
            messages.error(request, 'Error al guardar diagnóstico.')
    else:
        form = DiagnosticoTecnicoForm()

    return render(request, 'registrar_diagnostico.html', {'form': form, 'dispositivo': dispositivo})

from reportlab.pdfgen import canvas

@login_required
def generar_informe(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Informe_{dispositivo.numero_orden}.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Informe de Reparación N° {dispositivo.numero_orden}")
    p.drawString(100, 780, f"Cliente: {dispositivo.cliente.nombre}")
    p.drawString(100, 760, f"Dispositivo: {dispositivo.modelo}")

    if hasattr(dispositivo, 'diagnostico'):
        p.drawString(100, 720, "Diagnóstico:")
        p.drawString(120, 700, dispositivo.diagnostico.diagnostico[:80])
    else:
        p.drawString(100, 720, "Diagnóstico no registrado.")

    p.showPage()
    p.save()
    return response

# ⬇️ ⬇️ ⬇️ **AQUÍ SE AGREGA TU FUNCIÓN INVENTARIO SIN BORRAR NADA** ⬇️ ⬇️ ⬇️

@login_required
def inventario(request):
    items = Inventario.objects.all()

    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem agregado al inventario.")
            return redirect('inventario')
        else:
            messages.error(request, "Error en el formulario de inventario.")
    else:
        form = InventarioForm()

    return render(request, 'inventario.html', {'items': items, 'form': form})

