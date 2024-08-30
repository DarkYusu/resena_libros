from django import forms
from django.contrib.auth.models import User
from .models import Agenda, Cita, Especialista, CentroMedico, Perfil

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['fecha_disponible', 'hora_disponible', 'especialista', 'centro_medico']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: puedes añadir widgets o configuraciones adicionales
        self.fields['especialista'].queryset = Especialista.objects.all()
        self.fields['centro_medico'].queryset = CentroMedico.objects.all()

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mensaje']

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)
    
class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario']
        widgets = {
            'tipo_usuario': forms.RadioSelect,
        }
        
class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Tu email'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Tu mensaje', 'rows': 5}))