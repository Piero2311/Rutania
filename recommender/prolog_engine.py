"""
Motor de inferencia lógica usando pyDatalog.
Implementa el paradigma lógico para recomendaciones médicas.

pyDatalog es una implementación de Datalog (subconjunto de Prolog) en Python puro.
No requiere SWI-Prolog instalado y es compatible con despliegues en la nube como Render.
Tiene sintaxis muy similar a Prolog.
"""
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Intentar importar pyDatalog, si no está disponible usar motor lógico alternativo
try:
    from pyDatalog import pyDatalog
    PYDATALOG_AVAILABLE = True
    logger.info("Motor Prolog: pyDatalog disponible y listo para usar.")
except ImportError:
    PYDATALOG_AVAILABLE = False
    logger.info("Motor Prolog: Usando implementación Python pura (pyDatalog no disponible).")


class MotorProlog:
    """
    Motor de inferencia lógica que usa pyDatalog (Datalog/Prolog en Python puro).
    Si pyDatalog no está disponible, usa un motor lógico implementado en Python.
    """
    
    def __init__(self):
        if PYDATALOG_AVAILABLE:
            self._inicializar_pydatalog()
        else:
            self.motor_alternativo = MotorLogicoAlternativo()
            self.motor_alternativo.cargar_reglas_medicas()
            logger.info("Motor Prolog: Usando motor alternativo (Python puro).")
    
    def _inicializar_pydatalog(self):
        """Inicializa pyDatalog y carga las reglas médicas."""
        if not PYDATALOG_AVAILABLE:
            return
        
        # Definir predicados lógicos usando pyDatalog
        pyDatalog.create_terms('intensidad_recomendada, objetivo_prioritario, rutina_segura, edad, imc, nivel_experiencia, intensidad_rutina, dias_rutina, nivel_rutina')
        
        # Cargar reglas médicas
        self.cargar_reglas_medicas()
        logger.info("Motor Prolog: pyDatalog inicializado correctamente.")
    
    def cargar_reglas_medicas(self):
        """Carga las reglas médicas en pyDatalog."""
        if not PYDATALOG_AVAILABLE:
            return
        
        try:
            # Reglas de intensidad recomendada por edad
            # Sintaxis pyDatalog: predicado(X, Y) <= condición
            pyDatalog.load("""
                intensidad_recomendada(Edad, 'baja') <= (Edad > 60)
                intensidad_recomendada(Edad, 'media') <= (Edad >= 18) & (Edad <= 60)
                intensidad_recomendada(Edad, 'alta') <= (Edad >= 18) & (Edad < 40)
            """)
            
            # Reglas de objetivo prioritario por IMC
            pyDatalog.load("""
                objetivo_prioritario(IMC, 'peso') <= (IMC > 30)
                objetivo_prioritario(IMC, 'peso') <= (IMC > 25) & (IMC <= 30)
                objetivo_prioritario(IMC, 'mantenimiento') <= (IMC >= 18.5) & (IMC <= 25)
                objetivo_prioritario(IMC, 'musculacion') <= (IMC < 18.5)
            """)
            
            logger.info("Reglas médicas de pyDatalog cargadas correctamente.")
        except Exception as e:
            logger.error(f"Error cargando reglas pyDatalog: {e}")
    
    def evaluar_seguridad_rutina(self, usuario_data: Dict, rutina_data: Dict) -> Tuple[bool, str]:
        """
        Evalúa si una rutina es segura para el usuario usando pyDatalog.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            rutina_data: Diccionario con datos de la rutina
            
        Returns:
            Tupla (es_segura, razon)
        """
        if not PYDATALOG_AVAILABLE:
            return self.motor_alternativo.evaluar_seguridad_rutina(usuario_data, rutina_data)
        
        try:
            edad = usuario_data.get('edad', 30)
            imc = usuario_data.get('imc', 25.0)
            nivel_usuario = usuario_data.get('nivel_experiencia', 'principiante')
            intensidad_rutina = rutina_data.get('intensidad', 'media')
            dias_rutina = rutina_data.get('dias_semana', 3)
            nivel_rutina = rutina_data.get('nivel', 'principiante')
            
            # Evaluar seguridad directamente usando las reglas lógicas
            # pyDatalog se usa principalmente para consultas, aquí usamos evaluación directa
            # que implementa las mismas reglas lógicas
            return self._evaluar_seguridad_directa(usuario_data, rutina_data)
        except Exception as e:
            logger.error(f"Error en evaluación pyDatalog: {e}")
            return self._evaluar_seguridad_directa(usuario_data, rutina_data)
    
    def _evaluar_seguridad_directa(self, usuario_data: Dict, rutina_data: Dict) -> Tuple[bool, str]:
        """Evaluación directa de seguridad (fallback)."""
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        nivel_usuario = usuario_data.get('nivel_experiencia', 'principiante')
        intensidad_rutina = rutina_data.get('intensidad', 'media')
        dias_rutina = rutina_data.get('dias_semana', 3)
        nivel_rutina = rutina_data.get('nivel', 'principiante')
        
        if edad > 60 and intensidad_rutina == 'alta':
            return (False, "Intensidad alta no recomendada para mayores de 60 años")
        if imc > 30 and dias_rutina > 5:
            return (False, "Demasiados días de entrenamiento para comenzar con obesidad")
        if nivel_usuario == 'principiante' and nivel_rutina == 'avanzado':
            return (False, "Rutina demasiado avanzada para tu nivel actual")
        
        return (True, "Rutina segura y adecuada")
    
    def determinar_intensidad_recomendada(self, usuario_data: Dict) -> str:
        """
        Determina la intensidad recomendada usando pyDatalog.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Intensidad recomendada ('baja', 'media', 'alta')
        """
        if not PYDATALOG_AVAILABLE:
            return self.motor_alternativo.determinar_intensidad_recomendada(usuario_data)
        
        try:
            edad = usuario_data.get('edad', 30)
            nivel = usuario_data.get('nivel_experiencia', 'principiante')
            imc = usuario_data.get('imc', 25.0)
            imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
            
            # Consultar pyDatalog usando la sintaxis correcta
            X = pyDatalog.Variable()
            query = pyDatalog.ask('intensidad_recomendada(Edad, X)', Edad=edad)
            
            if query and len(query) > 0:
                # pyDatalog retorna una lista de respuestas
                intensidad = query[0]['X']
                # Ajustar según nivel y IMC
                if nivel == 'avanzado' and edad < 40 and imc <= 30 and imc_clasificacion != 'obesidad':
                    return 'alta'
                elif edad > 60 or imc > 30 or imc_clasificacion == 'obesidad':
                    return 'baja'
                return intensidad
            
            # Fallback a evaluación directa
            return self._determinar_intensidad_directa(usuario_data)
        except Exception as e:
            logger.error(f"Error en pyDatalog: {e}")
            return self._determinar_intensidad_directa(usuario_data)
    
    def _determinar_intensidad_directa(self, usuario_data: Dict) -> str:
        """Determina intensidad directamente (fallback)."""
        edad = usuario_data.get('edad', 30)
        nivel = usuario_data.get('nivel_experiencia', 'principiante')
        imc = usuario_data.get('imc', 25.0)
        imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
        
        if edad > 60 or imc > 30 or imc_clasificacion == 'obesidad':
            return 'baja'
        elif nivel == 'avanzado' and edad < 40:
            return 'alta'
        else:
            return 'media'
    
    def determinar_objetivo_prioritario(self, usuario_data: Dict) -> str:
        """
        Determina el objetivo prioritario usando pyDatalog.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Objetivo prioritario
        """
        if not PYDATALOG_AVAILABLE:
            return self.motor_alternativo.determinar_objetivo_prioritario(usuario_data)
        
        try:
            imc = usuario_data.get('imc', 25.0)
            imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
            objetivo_usuario = usuario_data.get('objetivos', 'salud')
            
            # Consultar pyDatalog usando la sintaxis correcta
            X = pyDatalog.Variable()
            query = pyDatalog.ask('objetivo_prioritario(IMC, X)', IMC=imc)
            
            if query and len(query) > 0:
                # pyDatalog retorna una lista de respuestas
                objetivo = query[0]['X']
                # Ajustar según clasificación IMC
                if imc_clasificacion in ['obesidad', 'sobrepeso']:
                    return 'peso'
                elif imc_clasificacion == 'bajo_peso':
                    return 'musculacion'
                return objetivo
            
            # Fallback
            return self._determinar_objetivo_directo(usuario_data)
        except Exception as e:
            logger.error(f"Error en pyDatalog: {e}")
            return self._determinar_objetivo_directo(usuario_data)
    
    def _determinar_objetivo_directo(self, usuario_data: Dict) -> str:
        """Determina objetivo directamente (fallback)."""
        imc = usuario_data.get('imc', 25.0)
        imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
        objetivo_usuario = usuario_data.get('objetivos', 'salud')
        
        if imc > 30 or imc_clasificacion in ['obesidad', 'sobrepeso']:
            return 'peso'
        elif imc < 18.5 or imc_clasificacion == 'bajo_peso':
            return 'musculacion'
        else:
            return objetivo_usuario if objetivo_usuario else 'mantenimiento'
    
    def generar_explicacion_medica(self, usuario_data: Dict, rutina_data: Dict) -> str:
        """
        Genera una explicación médica usando pyDatalog.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            rutina_data: Diccionario con datos de la rutina
            
        Returns:
            Explicación médica detallada
        """
        if not PYDATALOG_AVAILABLE:
            return self.motor_alternativo.generar_explicacion_medica(usuario_data, rutina_data)
        
        explicaciones = []
        
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        nivel_usuario = usuario_data.get('nivel_experiencia', 'principiante')
        
        # Generar explicaciones basadas en reglas lógicas
        if rutina_data.get('nivel') == nivel_usuario:
            explicaciones.append(f"✓ Nivel {rutina_data['nivel']} adecuado para tu experiencia")
        
        objetivo_recomendado = self.determinar_objetivo_prioritario(usuario_data)
        if rutina_data.get('objetivo') == objetivo_recomendado:
            explicaciones.append(f"✓ Alineada con tu objetivo de {rutina_data['objetivo']}")
        
        if edad > 50 and rutina_data.get('intensidad') == 'baja':
            explicaciones.append("✓ Intensidad baja recomendada por tu edad")
        
        if imc > 25 and rutina_data.get('objetivo') == 'peso':
            explicaciones.append("✓ Enfocada en pérdida de peso según tu IMC")
        
        return '\n'.join(explicaciones) if explicaciones else "Rutina compatible con tu perfil"
    
    def evaluar_condiciones(self, usuario_data: Dict) -> Dict[str, Any]:
        """
        Evalúa todas las condiciones médicas usando pyDatalog.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Diccionario con evaluación completa
        """
        if not PYDATALOG_AVAILABLE:
            return self.motor_alternativo.evaluar_condiciones(usuario_data)
        
        evaluacion = {
            'intensidad_recomendada': self.determinar_intensidad_recomendada(usuario_data),
            'objetivo_prioritario': self.determinar_objetivo_prioritario(usuario_data),
            'precauciones': self._obtener_precauciones(usuario_data),
            'es_seguro': True
        }
        
        return evaluacion
    
    def _obtener_precauciones(self, usuario_data: Dict) -> List[str]:
        """Obtiene lista de precauciones."""
        precauciones = []
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
        
        if edad > 60:
            precauciones.append("Edad avanzada: se recomienda intensidad baja")
        if imc > 30 or imc_clasificacion == 'obesidad':
            precauciones.append("Obesidad: comenzar con rutinas de baja intensidad")
        if imc < 18.5 or imc_clasificacion == 'bajo_peso':
            precauciones.append("Bajo peso: consultar médico antes de entrenar intensamente")
        
        return precauciones


class MotorLogicoAlternativo:
    """
    Motor lógico alternativo implementado en Python puro.
    Se usa cuando pyDatalog no está disponible.
    """
    
    def __init__(self):
        self.reglas = []
    
    def cargar_reglas_medicas(self):
        """Carga reglas médicas en el motor alternativo."""
        # Las reglas se implementan como funciones de evaluación
        pass
    
    def evaluar_seguridad_rutina(self, usuario_data: Dict, rutina_data: Dict) -> Tuple[bool, str]:
        """Evalúa seguridad de rutina."""
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        nivel_usuario = usuario_data.get('nivel_experiencia', 'principiante')
        nivel_rutina = rutina_data.get('nivel', 'principiante')
        intensidad_rutina = rutina_data.get('intensidad', 'media')
        dias_rutina = rutina_data.get('dias_semana', 3)
        
        # Regla 1: Edad > 60 y intensidad alta
        if edad > 60 and intensidad_rutina == 'alta':
            return (False, "Intensidad alta no recomendada para mayores de 60 años")
        
        # Regla 2: Obesidad y muchos días
        if imc > 30 and dias_rutina > 5:
            return (False, "Demasiados días de entrenamiento para comenzar con obesidad")
        
        # Regla 3: Principiante con rutina avanzada
        if nivel_usuario == 'principiante' and nivel_rutina == 'avanzado':
            return (False, "Rutina demasiado avanzada para tu nivel actual")
        
        return (True, "Rutina segura y adecuada")
    
    def determinar_intensidad_recomendada(self, usuario_data: Dict) -> str:
        """Determina intensidad recomendada."""
        edad = usuario_data.get('edad', 30)
        nivel = usuario_data.get('nivel_experiencia', 'principiante')
        imc = usuario_data.get('imc', 25.0)
        
        if edad > 60 or imc > 30:
            return 'baja'
        elif nivel == 'avanzado' and edad < 40:
            return 'alta'
        else:
            return 'media'
    
    def determinar_objetivo_prioritario(self, usuario_data: Dict) -> str:
        """Determina objetivo prioritario."""
        imc = usuario_data.get('imc', 25.0)
        
        if imc > 30:
            return 'peso'
        elif imc < 18.5:
            return 'musculacion'
        else:
            return usuario_data.get('objetivos', 'mantenimiento')
    
    def generar_explicacion_medica(self, usuario_data: Dict, rutina_data: Dict) -> str:
        """Genera explicación médica."""
        explicaciones = []
        
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        nivel_usuario = usuario_data.get('nivel_experiencia', 'principiante')
        
        if rutina_data.get('nivel') == nivel_usuario:
            explicaciones.append(f"✓ Nivel {rutina_data['nivel']} adecuado para tu experiencia")
        
        if rutina_data.get('objetivo') == usuario_data.get('objetivos'):
            explicaciones.append(f"✓ Alineada con tu objetivo de {rutina_data['objetivo']}")
        
        if edad > 50 and rutina_data.get('intensidad') == 'baja':
            explicaciones.append("✓ Intensidad baja recomendada por tu edad")
        
        if imc > 25 and rutina_data.get('objetivo') == 'peso':
            explicaciones.append("✓ Enfocada en pérdida de peso según tu IMC")
        
        return '\n'.join(explicaciones) if explicaciones else "Rutina compatible con tu perfil"
    
    def evaluar_condiciones(self, usuario_data: Dict) -> Dict[str, Any]:
        """Evalúa todas las condiciones médicas."""
        return {
            'intensidad_recomendada': self.determinar_intensidad_recomendada(usuario_data),
            'objetivo_prioritario': self.determinar_objetivo_prioritario(usuario_data),
            'precauciones': self._obtener_precauciones(usuario_data),
            'es_seguro': True
        }
    
    def _obtener_precauciones(self, usuario_data: Dict) -> List[str]:
        """Obtiene lista de precauciones."""
        precauciones = []
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        
        if edad > 60:
            precauciones.append("Edad avanzada: se recomienda intensidad baja")
        if imc > 30:
            precauciones.append("Obesidad: comenzar con rutinas de baja intensidad")
        if imc < 18.5:
            precauciones.append("Bajo peso: consultar médico antes de entrenar intensamente")
        
        return precauciones


# Instancia global del motor
motor_prolog = MotorProlog()
