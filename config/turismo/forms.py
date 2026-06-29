from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reserva, Cliente
from datetime import date

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombres')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_viaje', 'numero_personas', 'observaciones']
        widgets = {
            'fecha_viaje': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_fecha_viaje(self):
        fecha = self.cleaned_data['fecha_viaje']
        if fecha < date.today():
            raise forms.ValidationError('La fecha de viaje no puede ser en el pasado')
        return fecha


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'numero_documento', 'telefono', 'direccion']
