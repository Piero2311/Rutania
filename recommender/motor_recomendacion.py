"""
Motor de Recomendación Híbrido.
Integra los tres paradigmas: Imperativo, Funcional y Lógico.
"""
from typing import Dict, List, Optional, Tuple
from functools import reduce
from django.db.models import QuerySet

from .models import Rutina, UsuarioPersonalizado, RecomendacionMedica, PerfilMedico
from .processor import (
    calcular_imc, 
    clasificar_imc,
    calcular_compatibilidad,
    filtrar_rutinas_por_seguridad,
    calcular_calorias_estimadas
)
from .prolog_engine import motor_prolog


class MotorRecomendacion:
    """
    Motor de recomendación que integra los tres paradigmas:
    - Imperativo: Control de flujo y coordinación
    - Funcional: Transformaciones y filtrado
    - Lógico: Inferencia médica con Prolog
    """
    
    def __init__(self):
        self.motor_prolog = motor_prolog
    
    def generar_recomendacion_completa(self, usuario: UsuarioPersonalizado) -> Dict:
        """
        Genera una recomendación completa integrando los tres paradigmas.
        
        PARADIGMA IMPERATIVO: Control de flujo secuencial
        1. Validar datos del usuario
        2. Obtener perfil médico
        3. Coordinar módulos funcional y lógico
        4. Generar recomendación final
        
        Args:
            usuario: Instancia de UsuarioPersonalizado
            
        Returns:
            Diccionario con recomendación completa
        """
        # 1. Validación imperativa
        if not usuario.altura or not usuario.peso:
            raise ValueError("Usuario debe tener altura y peso registrados")
        
        # 2. Obtener o crear perfil médico
        perfil_medico, _ = PerfilMedico.objects.get_or_create(usuario=usuario)
        
        # 3. Actualizar perfil médico (funcional)
        self._actualizar_perfil_medico(usuario, perfil_medico)
        
        # 4. Análisis de perfil médico (lógico - Prolog)
        evaluacion_medica = self.motor_prolog.evaluar_condiciones(
            self._usuario_a_dict(usuario, perfil_medico)
        )
        
        # 5. Filtrado funcional de rutinas seguras
        todas_rutinas = Rutina.objects.filter(activa=True)
        
        # Si no hay rutinas, intentar cargarlas automáticamente
        if todas_rutinas.count() == 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("No hay rutinas en BD, intentando cargar desde datos.py")
            try:
                from django.core.management import call_command
                call_command('cargar_rutinas', verbosity=0)
                todas_rutinas = Rutina.objects.filter(activa=True)
                logger.info(f"Rutinas cargadas: {todas_rutinas.count()}")
            except Exception as e:
                logger.error(f"Error cargando rutinas: {str(e)}")
        
        if todas_rutinas.count() == 0:
            return {
                'error': 'No hay rutinas disponibles en el sistema. Por favor, contacta al administrador.',
                'precauciones': evaluacion_medica.get('precauciones', [])
            }
        
        rutinas_seguras = self._filtrar_rutinas_seguras(
            todas_rutinas,
            usuario,
            evaluacion_medica
        )
        
        if not rutinas_seguras:
            return {
                'error': 'No se encontraron rutinas seguras para tu perfil. Por favor, actualiza tu perfil médico.',
                'precauciones': evaluacion_medica.get('precauciones', [])
            }
        
        # 6. Cálculo de compatibilidad (funcional)
        rutinas_compatibles = self._calcular_compatibilidad_rutinas(
            rutinas_seguras,
            usuario,
            evaluacion_medica
        )
        
        if not rutinas_compatibles:
            return {
                'error': 'No se encontraron rutinas compatibles',
                'precauciones': evaluacion_medica.get('precauciones', [])
            }
        
        # 7. Selección de mejor rutina (imperativo)
        rutina_recomendada, score = rutinas_compatibles[0]
        
        # 8. Generación de explicación médica (lógico)
        explicacion = self.motor_prolog.generar_explicacion_medica(
            self._usuario_a_dict(usuario, perfil_medico),
            self._rutina_a_dict(rutina_recomendada)
        )
        
        # 9. Validación de seguridad final (lógico)
        es_seguro, razon_seguridad = self.motor_prolog.evaluar_seguridad_rutina(
            self._usuario_a_dict(usuario, perfil_medico),
            self._rutina_a_dict(rutina_recomendada)
        )
        
        # 10. Crear recomendación en BD (imperativo)
        recomendacion = RecomendacionMedica.objects.create(
            usuario=usuario,
            rutina_recomendada=rutina_recomendada,
            explicacion_medica=explicacion,
            precauciones='\n'.join(evaluacion_medica.get('precauciones', [])),
            objetivos_especificos=f"Objetivo: {evaluacion_medica.get('objetivo_prioritario', usuario.objetivos)}",
            score_confianza=score,
            reglas_aplicadas={
                'intensidad_recomendada': evaluacion_medica.get('intensidad_recomendada'),
                'objetivo_prioritario': evaluacion_medica.get('objetivo_prioritario'),
                'precauciones': evaluacion_medica.get('precauciones', [])
            }
        )
        
        # 11. Obtener rutinas alternativas (funcional)
        rutinas_alternativas = self._obtener_alternativas(
            rutinas_compatibles,
            rutina_recomendada,
            limite=3
        )
        
        return {
            'recomendacion': recomendacion,
            'rutina_recomendada': rutina_recomendada,
            'explicacion_medica': explicacion,
            'rutinas_alternativas': rutinas_alternativas,
            'precauciones': evaluacion_medica.get('precauciones', []),
            'es_seguro': es_seguro,
            'razon_seguridad': razon_seguridad,
            'score_confianza': score,
            'evaluacion_medica': evaluacion_medica
        }
    
    def _actualizar_perfil_medico(self, usuario: UsuarioPersonalizado, perfil: PerfilMedico):
        """
        Actualiza el perfil médico usando funciones puras (paradigma funcional).
        """
        if usuario.altura and usuario.peso:
            # Funciones puras
            altura_metros = usuario.altura / 100  # Convertir cm a metros
            imc = calcular_imc(usuario.peso, altura_metros)
            clasificacion = clasificar_imc(imc)
            
            perfil.imc = imc
            perfil.clasificacion_imc = clasificacion
            perfil.save()
    
    def _filtrar_rutinas_seguras(
        self, 
        rutinas: QuerySet, 
        usuario: UsuarioPersonalizado,
        evaluacion_medica: Dict
    ) -> List[Rutina]:
        """
        Filtra rutinas seguras usando paradigma funcional.
        """
        usuario_dict = self._usuario_a_dict(usuario)
        usuario_dict.update(evaluacion_medica)
        
        rutinas_lista = list(rutinas)
        
        # Filtrar por seguridad usando función pura
        def es_rutina_segura(rutina: Rutina) -> bool:
            rutina_dict = self._rutina_a_dict(rutina)
            es_seguro, _ = self.motor_prolog.evaluar_seguridad_rutina(
                usuario_dict,
                rutina_dict
            )
            return es_seguro
        
        # Usar filter (paradigma funcional)
        return list(filter(es_rutina_segura, rutinas_lista))
    
    def _calcular_compatibilidad_rutinas(
        self,
        rutinas: List[Rutina],
        usuario: UsuarioPersonalizado,
        evaluacion_medica: Dict
    ) -> List[Tuple[Rutina, float]]:
        """
        Calcula compatibilidad de rutinas usando paradigma funcional.
        """
        usuario_dict = self._usuario_a_dict(usuario)
        usuario_dict.update(evaluacion_medica)
        
        # Mapear rutinas a tuplas (rutina, score) usando map
        rutinas_puntuadas = list(map(
            lambda r: (
                r,
                calcular_compatibilidad(
                    self._rutina_a_dict(r),
                    usuario_dict
                )
            ),
            rutinas
        ))
        
        # Ordenar por score (funcional)
        return sorted(rutinas_puntuadas, key=lambda x: x[1], reverse=True)
    
    def _obtener_alternativas(
        self,
        rutinas_compatibles: List[Tuple[Rutina, float]],
        rutina_principal: Rutina,
        limite: int = 3
    ) -> List[Tuple[Rutina, float]]:
        """
        Obtiene rutinas alternativas usando paradigma funcional.
        """
        # Filtrar excluyendo la principal
        alternativas = list(filter(
            lambda x: x[0].id != rutina_principal.id,
            rutinas_compatibles
        ))
        
        return alternativas[:limite]
    
    def _usuario_a_dict(self, usuario: UsuarioPersonalizado, perfil: Optional[PerfilMedico] = None) -> Dict:
        """Convierte usuario a diccionario para procesamiento."""
        if perfil is None:
            try:
                perfil = usuario.perfil_medico
            except PerfilMedico.DoesNotExist:
                perfil = None
        
        edad = usuario.calcular_edad() if usuario.fecha_nacimiento else 30
        
        return {
            'id': usuario.id,
            'edad': edad,
            'peso': usuario.peso or 70.0,
            'altura': (usuario.altura or 170.0) / 100,  # Convertir a metros
            'imc': perfil.imc if perfil and perfil.imc else 25.0,
            'imc_clasificacion': perfil.clasificacion_imc if perfil else 'normal',
            'nivel_experiencia': usuario.nivel_experiencia,
            'objetivos': usuario.objetivos,
            'dias_disponibles': usuario.dias_entrenamiento,
            'condiciones_medicas': usuario.condiciones_medicas,
            'restricciones': usuario.restricciones
        }
    
    def _rutina_a_dict(self, rutina: Rutina) -> Dict:
        """Convierte rutina a diccionario para procesamiento."""
        return {
            'id': rutina.id,
            'nombre': rutina.nombre,
            'nivel': rutina.nivel,
            'objetivo': rutina.objetivo,
            'intensidad': rutina.intensidad,
            'dias_semana': rutina.dias_semana,
            'duracion': rutina.duracion,
            'calorias_estimadas': rutina.calorias_estimadas,
            'restricciones_medicas': rutina.restricciones_medicas
        }
    
    def calcular_progreso_promedio(self, usuario: UsuarioPersonalizado) -> Dict:
        """
        Calcula progreso promedio usando reduce (paradigma funcional).
        """
        seguimientos = usuario.seguimientos.all()
        
        if not seguimientos:
            return {
                'promedio_imc': 0,
                'total_seguimientos': 0,
                'tendencia': 'sin_datos'
            }
        
        # Usar reduce para calcular promedio
        suma_imc = reduce(
            lambda acc, s: acc + s.imc_actual,
            seguimientos,
            0.0
        )
        
        promedio_imc = suma_imc / len(seguimientos)
        
        # Calcular tendencia
        if len(seguimientos) >= 2:
            imc_inicial = seguimientos.last().imc_actual
            imc_final = seguimientos.first().imc_actual
            if imc_final < imc_inicial:
                tendencia = 'mejora'
            elif imc_final > imc_inicial:
                tendencia = 'empeora'
            else:
                tendencia = 'estable'
        else:
            tendencia = 'insuficiente_datos'
        
        return {
            'promedio_imc': round(promedio_imc, 2),
            'total_seguimientos': len(seguimientos),
            'tendencia': tendencia
        }


# Instancia global del motor
motor_recomendacion = MotorRecomendacion()

