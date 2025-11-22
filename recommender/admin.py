from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UsuarioPersonalizado,
    PerfilMedico,
    Rutina,
    RecomendacionMedica,
    SeguimientoUsuario
)


@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    """Admin personalizado para UsuarioPersonalizado."""
    list_display = ('username', 'email', 'fecha_nacimiento', 'altura', 'peso', 'objetivos', 'nivel_experiencia', 'fecha_registro')
    list_filter = ('objetivos', 'nivel_experiencia', 'fecha_registro')
    search_fields = ('username', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Deportiva', {
            'fields': ('fecha_nacimiento', 'altura', 'peso', 'objetivos', 'nivel_experiencia', 'dias_entrenamiento')
        }),
        ('Información Médica', {
            'fields': ('condiciones_medicas', 'restricciones')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal', {
            'fields': ('email', 'fecha_nacimiento', 'altura', 'peso')
        }),
        ('Información Deportiva', {
            'fields': ('objetivos', 'nivel_experiencia', 'dias_entrenamiento')
        }),
    )


@admin.register(PerfilMedico)
class PerfilMedicoAdmin(admin.ModelAdmin):
    """Admin para PerfilMedico."""
    list_display = ('usuario', 'imc', 'clasificacion_imc', 'frecuencia_cardiaca', 'fecha_actualizacion')
    list_filter = ('clasificacion_imc', 'fecha_actualizacion')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('fecha_actualizacion', 'imc', 'clasificacion_imc')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Métricas Médicas', {
            'fields': ('imc', 'clasificacion_imc', 'presion_arterial', 'frecuencia_cardiaca')
        }),
        ('Historial Médico', {
            'fields': ('alergias', 'medicamentos', 'historial_lesiones')
        }),
        ('Metadata', {
            'fields': ('fecha_actualizacion',)
        }),
    )


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    """Admin para Rutina."""
    list_display = ('nombre', 'nivel', 'objetivo', 'intensidad', 'dias_semana', 'calorias_estimadas', 'activa', 'fecha_creacion')
    list_filter = ('nivel', 'objetivo', 'intensidad', 'activa', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'activa')
        }),
        ('Características', {
            'fields': ('nivel', 'objetivo', 'intensidad', 'dias_semana', 'duracion')
        }),
        ('Ejercicios', {
            'fields': ('ejercicios',)
        }),
        ('Métricas', {
            'fields': ('calorias_estimadas',)
        }),
        ('Restricciones', {
            'fields': ('restricciones_medicas',)
        }),
        ('Metadata', {
            'fields': ('fecha_creacion',)
        }),
    )


@admin.register(RecomendacionMedica)
class RecomendacionMedicaAdmin(admin.ModelAdmin):
    """Admin para RecomendacionMedica."""
    list_display = ('usuario', 'rutina_recomendada', 'score_confianza', 'vigente', 'fecha_recomendacion')
    list_filter = ('vigente', 'fecha_recomendacion', 'rutina_recomendada__nivel')
    search_fields = ('usuario__username', 'rutina_recomendada__nombre')
    readonly_fields = ('fecha_recomendacion',)
    
    fieldsets = (
        ('Usuario y Rutina', {
            'fields': ('usuario', 'rutina_recomendada', 'vigente')
        }),
        ('Recomendación', {
            'fields': ('explicacion_medica', 'precauciones', 'objetivos_especificos')
        }),
        ('Análisis del Motor', {
            'fields': ('reglas_aplicadas', 'score_confianza')
        }),
        ('Metadata', {
            'fields': ('fecha_recomendacion',)
        }),
    )


@admin.register(SeguimientoUsuario)
class SeguimientoUsuarioAdmin(admin.ModelAdmin):
    """Admin para SeguimientoUsuario."""
    list_display = ('usuario', 'fecha', 'peso_actual', 'imc_actual', 'satisfaccion', 'rutina_realizada')
    list_filter = ('fecha', 'satisfaccion', 'rutina_realizada')
    search_fields = ('usuario__username', 'comentarios')
    readonly_fields = ('fecha', 'imc_actual')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Usuario y Fecha', {
            'fields': ('usuario', 'fecha')
        }),
        ('Métricas', {
            'fields': ('peso_actual', 'imc_actual')
        }),
        ('Rutina y Evaluación', {
            'fields': ('rutina_realizada', 'satisfaccion', 'comentarios')
        }),
    )
