"""
Formularios Django para el sistema de recomendación.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UsuarioPersonalizado, PerfilMedico, SeguimientoUsuario


class FormularioRegistro(UserCreationForm):
    """
    Formulario de registro personalizado que extiende UserCreationForm.
    Incluye campos médicos y deportivos.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Fecha de nacimiento"
    )
    altura = forms.FloatField(
        required=True,
        min_value=50.0,
        max_value=250.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Altura en cm (ej: 175)',
            'step': '0.1'
        }),
        help_text="Altura en centímetros"
    )
    peso = forms.FloatField(
        required=True,
        min_value=20.0,
        max_value=300.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Peso en kg (ej: 70)',
            'step': '0.1'
        }),
        help_text="Peso en kilogramos"
    )
    objetivos = forms.ChoiceField(
        required=True,
        choices=[('', 'Selecciona un objetivo')] + [
            ('peso', 'Pérdida de Peso'),
            ('musculacion', 'Ganancia de Músculo'),
            ('mantenimiento', 'Mantenimiento'),
            ('resistencia', 'Resistencia'),
            ('flexibilidad', 'Flexibilidad'),
            ('salud', 'Salud General'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Objetivo principal de entrenamiento"
    )
    nivel_experiencia = forms.ChoiceField(
        required=True,
        choices=[('', 'Selecciona un nivel')] + [
            ('principiante', 'Principiante'),
            ('intermedio', 'Intermedio'),
            ('avanzado', 'Avanzado'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Nivel de experiencia"
    )
    dias_entrenamiento = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=7,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Días disponibles por semana'
        }),
        help_text="Días disponibles para entrenar por semana"
    )
    condiciones_medicas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ej: Hipertensión, Diabetes, etc. (opcional)'
        }),
        help_text="Condiciones médicas conocidas (opcional)"
    )
    restricciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Restricciones físicas o médicas (opcional)'
        }),
        help_text="Restricciones adicionales (opcional)"
    )
    
    class Meta:
        model = UsuarioPersonalizado
        fields = (
            'username', 'email', 'password1', 'password2',
            'fecha_nacimiento', 'altura', 'peso', 'objetivos',
            'nivel_experiencia', 'dias_entrenamiento',
            'condiciones_medicas', 'restricciones'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        user.altura = self.cleaned_data['altura']
        user.peso = self.cleaned_data['peso']
        user.objetivos = self.cleaned_data['objetivos']
        user.nivel_experiencia = self.cleaned_data['nivel_experiencia']
        user.dias_entrenamiento = self.cleaned_data['dias_entrenamiento']
        user.condiciones_medicas = self.cleaned_data.get('condiciones_medicas', '')
        user.restricciones = self.cleaned_data.get('restricciones', '')
        
        if commit:
            user.save()
            # Crear perfil médico automáticamente
            from .motor_recomendacion import motor_recomendacion
            perfil, _ = PerfilMedico.objects.get_or_create(usuario=user)
            motor_recomendacion._actualizar_perfil_medico(user, perfil)
        
        return user


class FormularioPerfilMedico(forms.ModelForm):
    """
    Formulario para actualizar perfil médico.
    """
    class Meta:
        model = PerfilMedico
        fields = [
            'presion_arterial',
            'frecuencia_cardiaca',
            'alergias',
            'medicamentos',
            'historial_lesiones'
        ]
        widgets = {
            'presion_arterial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 120/80'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Frecuencia cardíaca en reposo (bpm)'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Alergias conocidas'
            }),
            'medicamentos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Medicamentos actuales'
            }),
            'historial_lesiones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Historial de lesiones previas'
            }),
        }


class FormularioActualizarUsuario(forms.ModelForm):
    """
    Formulario para actualizar datos básicos del usuario.
    """
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'altura',
            'peso',
            'objetivos',
            'nivel_experiencia',
            'dias_entrenamiento',
            'condiciones_medicas',
            'restricciones'
        ]
        widgets = {
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'objetivos': forms.Select(attrs={'class': 'form-control'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-control'}),
            'dias_entrenamiento': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'condiciones_medicas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'restricciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


class FormularioSeguimiento(forms.ModelForm):
    """
    Formulario para registrar seguimiento de progreso.
    """
    class Meta:
        model = SeguimientoUsuario
        fields = [
            'peso_actual',
            'rutina_realizada',
            'satisfaccion',
            'comentarios'
        ]
        widgets = {
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Peso actual en kg'
            }),
            'rutina_realizada': forms.Select(attrs={'class': 'form-control'}),
            'satisfaccion': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comentarios sobre tu progreso (opcional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            # Filtrar rutinas activas de las recomendaciones del usuario
            from .models import Rutina
            rutinas_ids = usuario.recomendaciones.filter(
                vigente=True
            ).values_list('rutina_recomendada_id', flat=True)
            self.fields['rutina_realizada'].queryset = Rutina.objects.filter(
                id__in=rutinas_ids, activa=True
            )
    
    def save(self, commit=True, usuario=None):
        seguimiento = super().save(commit=False)
        if usuario:
            seguimiento.usuario = usuario
            # Calcular IMC automáticamente
            if usuario.altura:
                altura_metros = usuario.altura / 100
                from .processor import calcular_imc
                seguimiento.imc_actual = calcular_imc(seguimiento.peso_actual, altura_metros)
        if commit:
            seguimiento.save()
        return seguimiento

