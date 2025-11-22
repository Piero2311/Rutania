from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Opciones para campos de elección
OBJETIVOS_OPCIONES = [
    ('peso', 'Pérdida de Peso'),
    ('musculacion', 'Ganancia de Músculo'),
    ('mantenimiento', 'Mantenimiento'),
    ('resistencia', 'Resistencia'),
    ('flexibilidad', 'Flexibilidad'),
    ('salud', 'Salud General'),
]

NIVEL_OPCIONES = [
    ('principiante', 'Principiante'),
    ('intermedio', 'Intermedio'),
    ('avanzado', 'Avanzado'),
]

INTENSIDAD_OPCIONES = [
    ('baja', 'Baja'),
    ('media', 'Media'),
    ('alta', 'Alta'),
]


class UsuarioPersonalizado(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Incluye campos adicionales para perfil deportivo y médico.
    """
    # Campos adicionales para perfil deportivo
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text="Fecha de nacimiento")
    altura = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(50.0), MaxValueValidator(250.0)],
        help_text="Altura en cm"
    )
    peso = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(20.0), MaxValueValidator(300.0)],
        help_text="Peso en kg"
    )
    condiciones_medicas = models.TextField(
        blank=True, 
        help_text="Condiciones médicas conocidas (separadas por comas)"
    )
    objetivos = models.CharField(
        max_length=100, 
        choices=OBJETIVOS_OPCIONES,
        default='salud',
        help_text="Objetivo principal de entrenamiento"
    )
    nivel_experiencia = models.CharField(
        max_length=20, 
        choices=NIVEL_OPCIONES,
        default='principiante',
        help_text="Nivel de experiencia en entrenamiento"
    )
    dias_entrenamiento = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Días disponibles para entrenar por semana"
    )
    restricciones = models.TextField(
        blank=True,
        help_text="Restricciones físicas o médicas adicionales"
    )
    
    # Metadata
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(auto_now=True)
    
    # Configuración seguridad
    REQUIRED_FIELDS = ['email', 'fecha_nacimiento']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def calcular_edad(self):
        """Calcula la edad del usuario en años."""
        if self.fecha_nacimiento:
            today = timezone.now().date()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None


class PerfilMedico(models.Model):
    """
    Perfil médico detallado del usuario.
    Se actualiza automáticamente cuando cambian peso/altura.
    """
    usuario = models.OneToOneField(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE,
        related_name='perfil_medico'
    )
    imc = models.FloatField(
        null=True,
        blank=True,
        help_text="Índice de Masa Corporal calculado"
    )
    clasificacion_imc = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clasificación del IMC (bajo_peso, normal, sobrepeso, obesidad)"
    )
    presion_arterial = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Presión arterial (ej: 120/80)"
    )
    frecuencia_cardiaca = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(40), MaxValueValidator(220)],
        help_text="Frecuencia cardíaca en reposo (bpm)"
    )
    alergias = models.TextField(
        blank=True,
        help_text="Alergias conocidas"
    )
    medicamentos = models.TextField(
        blank=True,
        help_text="Medicamentos actuales"
    )
    historial_lesiones = models.TextField(
        blank=True,
        help_text="Historial de lesiones previas"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil Médico'
        verbose_name_plural = 'Perfiles Médicos'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Perfil médico de {self.usuario.username}"


class Rutina(models.Model):
    """
    Modelo de rutina deportiva con ejercicios estructurados.
    """
    nombre = models.CharField(max_length=200, help_text="Nombre de la rutina")
    descripcion = models.TextField(help_text="Descripción detallada de la rutina")
    dias_semana = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="Días de entrenamiento por semana"
    )
    nivel = models.CharField(
        max_length=20, 
        choices=NIVEL_OPCIONES,
        help_text="Nivel de dificultad requerido"
    )
    objetivo = models.CharField(
        max_length=20, 
        choices=OBJETIVOS_OPCIONES,
        help_text="Objetivo principal de la rutina"
    )
    ejercicios = models.JSONField(
        help_text="Lista de ejercicios estructurados como JSON"
    )
    duracion = models.CharField(
        max_length=50,
        help_text="Duración estimada por sesión (ej: 45 minutos)"
    )
    intensidad = models.CharField(
        max_length=20,
        choices=INTENSIDAD_OPCIONES,
        help_text="Nivel de intensidad"
    )
    calorias_estimadas = models.IntegerField(
        default=0,
        help_text="Calorías estimadas quemadas por sesión"
    )
    restricciones_medicas = models.TextField(
        blank=True,
        help_text="Condiciones médicas que contraindican esta rutina"
    )
    
    # Metadata
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.nivel})"


class RecomendacionMedica(models.Model):
    """
    Recomendaciones médicas personalizadas generadas por el motor lógico.
    """
    usuario = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    rutina_recomendada = models.ForeignKey(
        Rutina, 
        on_delete=models.CASCADE,
        related_name='recomendaciones'
    )
    explicacion_medica = models.TextField(
        help_text="Explicación médica de por qué se recomienda esta rutina"
    )
    precauciones = models.TextField(
        blank=True,
        help_text="Precauciones específicas para el usuario"
    )
    objetivos_especificos = models.TextField(
        help_text="Objetivos específicos a alcanzar con esta rutina"
    )
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    vigente = models.BooleanField(
        default=True,
        help_text="Indica si la recomendación sigue siendo válida"
    )
    
    # Resultados del motor lógico Prolog
    reglas_aplicadas = models.JSONField(
        default=dict,
        help_text="Reglas lógicas aplicadas para generar esta recomendación"
    )
    score_confianza = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Score de confianza de la recomendación (0-100)"
    )
    
    class Meta:
        verbose_name = 'Recomendación Médica'
        verbose_name_plural = 'Recomendaciones Médicas'
        ordering = ['-fecha_recomendacion']
    
    def __str__(self):
        return f"Recomendación para {self.usuario.username} - {self.rutina_recomendada.nombre}"


class SeguimientoUsuario(models.Model):
    """
    Historial de seguimiento del progreso del usuario.
    """
    SATISFACCION_CHOICES = [
        (1, 'Muy Insatisfecho'),
        (2, 'Insatisfecho'),
        (3, 'Neutral'),
        (4, 'Satisfecho'),
        (5, 'Muy Satisfecho'),
    ]
    
    usuario = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )
    fecha = models.DateField(auto_now_add=True)
    peso_actual = models.FloatField(
        validators=[MinValueValidator(20.0), MaxValueValidator(300.0)],
        help_text="Peso actual en kg"
    )
    imc_actual = models.FloatField(
        help_text="IMC calculado en esta fecha"
    )
    rutina_realizada = models.ForeignKey(
        Rutina, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='seguimientos'
    )
    satisfaccion = models.IntegerField(
        choices=SATISFACCION_CHOICES,
        default=3,
        help_text="Nivel de satisfacción con la rutina"
    )
    comentarios = models.TextField(
        blank=True,
        help_text="Comentarios adicionales del usuario"
    )
    
    class Meta:
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Seguimiento de {self.usuario.username} - {self.fecha}"
