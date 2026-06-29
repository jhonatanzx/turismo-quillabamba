from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Cliente, PaqueteTuristico, Reserva
from .forms import RegistroForm, ReservaForm, ClienteForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {username}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'turismo/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(
                user=user,
                numero_documento=user.username,
                nombres=user.first_name,
                apellidos=user.last_name,
                email=user.email,
            )
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'turismo/registro.html', {'form': form})


def inicio(request):
    paquetes_recientes = PaqueteTuristico.objects.filter(activo=True)[:6]
    return render(request, 'turismo/inicio.html', {
        'paquetes_recientes': paquetes_recientes
    })


def lista_paquetes(request):
    paquetes = PaqueteTuristico.objects.filter(activo=True)

    busqueda = request.GET.get('busqueda')
    if busqueda:
        paquetes = paquetes.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(categoria__icontains=busqueda)
        )

    categoria = request.GET.get('categoria')
    if categoria:
        paquetes = paquetes.filter(categoria=categoria)

    return render(request, 'turismo/lista_paquetes.html', {
        'paquetes': paquetes,
        'categorias': PaqueteTuristico.CATEGORIAS,
    })


def detalle_paquete(request, pk):
    paquete = get_object_or_404(PaqueteTuristico, pk=pk, activo=True)
    return render(request, 'turismo/detalle_paquete.html', {'paquete': paquete})


@login_required
def crear_reserva(request, paquete_id):
    paquete = get_object_or_404(PaqueteTuristico, pk=paquete_id, activo=True)
    cliente = Cliente.objects.get(user=request.user)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente
            reserva.paquete = paquete
            reserva.precio_total = paquete.precio_por_persona * form.cleaned_data['numero_personas']
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente')
            return redirect('mis_reservas')
    else:
        form = ReservaForm()

    return render(request, 'turismo/crear_reserva.html', {
        'paquete': paquete,
        'form': form
    })


@login_required
def mis_reservas(request):
    cliente = Cliente.objects.get(user=request.user)
    reservas = Reserva.objects.filter(cliente=cliente).order_by('-fecha_reserva')
    return render(request, 'turismo/mis_reservas.html', {'reservas': reservas})


@login_required
def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente__user=request.user)
    return render(request, 'turismo/detalle_reserva.html', {'reserva': reserva})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente__user=request.user)

    if reserva.estado == 'CANCELADA':
        messages.warning(request, 'Esta reserva ya está cancelada')
        return redirect('mis_reservas')

    if request.method == 'POST':
        reserva.estado = 'CANCELADA'
        reserva.save()
        messages.success(request, 'Reserva cancelada exitosamente')
        return redirect('mis_reservas')

    return render(request, 'turismo/cancelar_reserva.html', {'reserva': reserva})


@login_required
def reporte_reservas(request):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver este reporte')
        return redirect('inicio')

    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    total_reservas = reservas.count()
    total_ingresos = sum(r.precio_total for r in reservas)

    estado = request.GET.get('estado')
    if estado:
        reservas = reservas.filter(estado=estado)

    return render(request, 'turismo/reporte_reservas.html', {
        'reservas': reservas,
        'total_reservas': total_reservas,
        'total_ingresos': total_ingresos,
        'estados': Reserva.ESTADOS,
    })


@login_required
def perfil_view(request):
    cliente = Cliente.objects.get(user=request.user)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('perfil')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'turismo/perfil.html', {'form': form})
