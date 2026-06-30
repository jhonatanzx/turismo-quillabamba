from django import forms
from .models import Reserva, Cliente
from django.core.exceptions import ValidationError
from datetime import date

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'numero_personas', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def clean_fecha_inicio(self):
        fecha = self.cleaned_data['fecha_inicio']
        if fecha < date.today():
            raise ValidationError('La fecha de inicio no puede ser en el pasado')
        return fecha
    
    def clean_numero_personas(self):
        num = self.cleaned_data['numero_personas']
        if num < 1:
            raise ValidationError('Debe ser al menos 1 persona')
        if num > 20:
            raise ValidationError('Máximo 20 personas por reserva')
        return num

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'numero_documento', 'nombres', 'apellidos', 'telefono', 'email', 'direccion']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }