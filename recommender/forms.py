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
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
            'type': 'date'
        }),
        help_text="Fecha de nacimiento"
    )
    altura = forms.FloatField(
        required=True,
        min_value=50.0,
        max_value=250.0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all'}),
        help_text="Objetivo principal de entrenamiento"
    )
    nivel_experiencia = forms.ChoiceField(
        required=True,
        choices=[('', 'Selecciona un nivel')] + [
            ('principiante', 'Principiante'),
            ('intermedio', 'Intermedio'),
            ('avanzado', 'Avanzado'),
        ],
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all'}),
        help_text="Nivel de experiencia"
    )
    dias_entrenamiento = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=7,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
            'placeholder': 'Días disponibles por semana'
        }),
        help_text="Días disponibles para entrenar por semana"
    )
    condiciones_salud = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('hipertension', 'Hipertensión'),
            ('diabetes', 'Diabetes'),
            ('problemas_cardiacos', 'Problemas Cardíacos'),
            ('artritis', 'Artritis'),
            ('osteoporosis', 'Osteoporosis'),
            ('lesion_rodilla', 'Lesión de Rodilla'),
            ('lesion_espalda', 'Lesión de Espalda'),
            ('asma', 'Asma'),
            ('embarazo', 'Embarazo'),
            ('hernia_discal', 'Hernia Discal'),
            ('problemas_articulares', 'Problemas Articulares'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        help_text="Selecciona las condiciones de salud que aplican (si las tienes, algunas rutinas se restringirán automáticamente)"
    )
    condiciones_medicas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
            'rows': 2,
            'placeholder': 'Otras condiciones médicas o información adicional (opcional)'
        }),
        help_text="Otras condiciones médicas o información adicional (opcional)"
    )
    restricciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
            'condiciones_salud', 'condiciones_medicas', 'restricciones'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
        user.condiciones_salud = self.cleaned_data.get('condiciones_salud', [])
        user.condiciones_medicas = self.cleaned_data.get('condiciones_medicas', '')
        user.restricciones = self.cleaned_data.get('restricciones', '')
        
        if commit:
            try:
                # Guardar usuario
                user.save()
                
                # Crear perfil médico automáticamente
                perfil, created = PerfilMedico.objects.get_or_create(usuario=user)
                
                # Actualizar perfil médico con datos básicos
                from .processor import calcular_imc, clasificar_imc
                if user.altura and user.peso:
                    altura_metros = user.altura / 100
                    imc = calcular_imc(user.peso, altura_metros)
                    imc_clasificacion = clasificar_imc(imc)
                    perfil.imc = imc
                    perfil.clasificacion_imc = imc_clasificacion
                    perfil.save()
                    
            except Exception as e:
                # Si hay error, no fallar silenciosamente
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error al guardar usuario o perfil médico: {str(e)}", exc_info=True)
                # Re-lanzar la excepción para que se muestre al usuario
                raise
        
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
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'placeholder': 'Ej: 120/80'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'placeholder': 'Frecuencia cardíaca en reposo (bpm)'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'rows': 2,
                'placeholder': 'Alergias conocidas'
            }),
            'medicamentos': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'rows': 2,
                'placeholder': 'Medicamentos actuales'
            }),
            'historial_lesiones': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
            'condiciones_salud',
            'condiciones_medicas',
            'restricciones'
        ]
        widgets = {
            'altura': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'step': '0.1'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'step': '0.1'
            }),
            'objetivos': forms.Select(attrs={'class': 'form-control'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-control'}),
            'dias_entrenamiento': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'condiciones_medicas': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'rows': 3
            }),
            'restricciones': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
                'step': '0.1',
                'placeholder': 'Peso actual en kg'
            }),
            'rutina_realizada': forms.Select(attrs={'class': 'form-control'}),
            'satisfaccion': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-emerald focus:border-transparent transition-all',
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

