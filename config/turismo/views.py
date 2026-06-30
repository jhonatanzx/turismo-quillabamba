from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import PaqueteTuristico, Reserva, Cliente
from .forms import ReservaForm, ClienteForm

def lista_paquetes(request):
    paquetes = PaqueteTuristico.objects.filter(activo=True)
    
    categoria = request.GET.get('categoria')
    if categoria:
        paquetes = paquetes.filter(categoria=categoria)
    
    busqueda = request.GET.get('busqueda')
    if busqueda:
        paquetes = paquetes.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda)
        )
    
    context = {
        'paquetes': paquetes,
        'categorias': PaqueteTuristico.CATEGORIAS,
    }
    return render(request, 'turismo/inicio.html', context)

def detalle_paquete(request, pk):
    paquete = get_object_or_404(PaqueteTuristico, pk=pk, activo=True)
    itinerarios = paquete.itinerarios.all().order_by('dia')
    disponibilidad = paquete.cupos_restantes()
    
    context = {
        'paquete': paquete,
        'itinerarios': itinerarios,
        'disponibilidad': disponibilidad,
    }
    return render(request, 'turismo/detalle_paquete.html', context)

@login_required
def crear_reserva(request, paquete_id):
    paquete = get_object_or_404(PaqueteTuristico, pk=paquete_id, activo=True)
    
    cliente, created = Cliente.objects.get_or_create(
        user=request.user,
        defaults={
            'numero_documento': request.user.username,
            'nombres': request.user.first_name,
            'apellidos': request.user.last_name,
            'email': request.user.email,
        }
    )
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente
            reserva.paquete = paquete
            reserva.precio_total = paquete.precio_por_persona * form.cleaned_data['numero_personas']
            
            if paquete.cupos_restantes() < form.cleaned_data['numero_personas']:
                messages.error(request, 'No hay suficientes cupos disponibles')
                return redirect('turismo:detalle_paquete', pk=paquete_id)
            
            reserva.save()
            messages.success(request, f'Reserva creada exitosamente. Código: {reserva.codigo_reserva}')
            return redirect('turismo:detalle_reserva', codigo=reserva.codigo_reserva)
    else:
        form = ReservaForm()
    
    context = {
        'paquete': paquete,
        'form': form,
    }
    return render(request, 'turismo/crear_reserva.html', context)

@login_required
def detalle_reserva(request, codigo):
    reserva = get_object_or_404(Reserva, codigo_reserva=codigo)
    
    if reserva.cliente.user != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta reserva')
        return redirect('turismo:lista_paquetes')
    
    context = {'reserva': reserva}
    return render(request, 'turismo/detalle_reserva.html', context)

@login_required
def mis_reservas(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    reservas = Reserva.objects.filter(cliente=cliente).order_by('-fecha_reserva')
    
    context = {'reservas': reservas}
    return render(request, 'turismo/mis_reservas.html', context)

@login_required
def cancelar_reserva(request, codigo):
    reserva = get_object_or_404(Reserva, codigo_reserva=codigo)
    
    if reserva.cliente.user != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para cancelar esta reserva')
        return redirect('turismo:detalle_reserva', codigo=codigo)
    
    if reserva.estado not in ['PENDIENTE', 'CONFIRMADA']:
        messages.error(request, 'Esta reserva no se puede cancelar')
        return redirect('turismo:detalle_reserva', codigo=codigo)
    
    if request.method == 'POST':
        reserva.estado = 'CANCELADA'
        reserva.motivo_cancelacion = request.POST.get('motivo', 'Cancelado por el cliente')
        reserva.save()
        messages.success(request, 'Reserva cancelada exitosamente')
        return redirect('turismo:mis_reservas')
    
    context = {'reserva': reserva}
    return render(request, 'turismo/cancelar_reserva.html', context)

def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Registro exitoso. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = ClienteForm()
    
    context = {'form': form}
    return render(request, 'turismo/registro_cliente.html', context)

@login_required
def perfil_cliente(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('turismo:perfil_cliente')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {'form': form}
    return render(request, 'turismo/perfil_cliente.html', context)