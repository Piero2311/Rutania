"""
Motor de inferencia lógica usando Prolog.
Implementa el paradigma lógico para recomendaciones médicas.
"""
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# Intentar importar pyswip, si no está disponible usar motor lógico alternativo
try:
    from pyswip import Prolog
    PROLOG_AVAILABLE = True
except ImportError:
    PROLOG_AVAILABLE = False
    logger.warning("pyswip no disponible. Usando motor lógico alternativo.")


class MotorProlog:
    """
    Motor de inferencia lógica que integra con Prolog.
    Si pyswip no está disponible, usa un motor lógico implementado en Python.
    """
    
    def __init__(self):
        if PROLOG_AVAILABLE:
            self.engine = Prolog()
            self.cargar_reglas_medicas()
        else:
            self.engine = None
            self.motor_alternativo = MotorLogicoAlternativo()
            self.motor_alternativo.cargar_reglas_medicas()
    
    def cargar_reglas_medicas(self):
        """Carga las reglas médicas en el motor Prolog."""
        if PROLOG_AVAILABLE and self.engine:
            reglas = """
            % Reglas de seguridad por condiciones médicas
            rutina_segura(Usuario, Rutina) :-
                tiene_condicion(Usuario, Condicion),
                not contraindica_rutina(Rutina, Condicion).
            
            % Reglas de intensidad por edad
            intensidad_recomendada(Usuario, baja) :-
                edad(Usuario, Edad), Edad > 60.
            
            intensidad_recomendada(Usuario, moderada) :-
                edad(Usuario, Edad), Edad >= 18, Edad =< 60.
            
            intensidad_recomendada(Usuario, alta) :-
                edad(Usuario, Edad), Edad >= 18, Edad < 40,
                nivel_experiencia(Usuario, avanzado).
            
            % Reglas por IMC
            objetivo_prioritario(Usuario, perdida_peso) :-
                imc(Usuario, IMC), IMC > 30.
            
            objetivo_prioritario(Usuario, mantenimiento) :-
                imc(Usuario, IMC), IMC >= 18.5, IMC =< 25.
            
            objetivo_prioritario(Usuario, ganancia_musculo) :-
                imc(Usuario, IMC), IMC < 18.5.
            
            % Reglas de compatibilidad
            rutina_compatible(Usuario, Rutina) :-
                nivel_usuario(Usuario, Nivel),
                nivel_rutina(Rutina, Nivel),
                objetivo_usuario(Usuario, Objetivo),
                objetivo_rutina(Rutina, Objetivo).
            
            % Reglas de precauciones
            requiere_precaucion(Usuario, Rutina, Precaucion) :-
                edad(Usuario, Edad), Edad > 50,
                intensidad_rutina(Rutina, alta),
                Precaucion = 'Intensidad alta no recomendada para mayores de 50 años'.
            
            requiere_precaucion(Usuario, Rutina, Precaucion) :-
                imc(Usuario, IMC), IMC > 30,
                dias_rutina(Rutina, Dias), Dias > 5,
                Precaucion = 'Demasiados días de entrenamiento para comenzar con obesidad'.
            """
            try:
                for regla in reglas.strip().split('\n'):
                    if regla.strip() and not regla.strip().startswith('%'):
                        self.engine.assertz(regla)
            except Exception as e:
                logger.error(f"Error cargando reglas Prolog: {e}")
    
    def evaluar_seguridad_rutina(self, usuario_data: Dict, rutina_data: Dict) -> Tuple[bool, str]:
        """
        Evalúa si una rutina es segura para el usuario.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            rutina_data: Diccionario con datos de la rutina
            
        Returns:
            Tupla (es_segura, razon)
        """
        if PROLOG_AVAILABLE and self.engine:
            return self._evaluar_con_prolog(usuario_data, rutina_data)
        else:
            return self.motor_alternativo.evaluar_seguridad_rutina(usuario_data, rutina_data)
    
    def _evaluar_con_prolog(self, usuario_data: Dict, rutina_data: Dict) -> Tuple[bool, str]:
        """Evalúa usando Prolog real."""
        try:
            # Preparar hechos
            edad = usuario_data.get('edad', 0)
            imc = usuario_data.get('imc', 25.0)
            nivel = usuario_data.get('nivel_experiencia', 'principiante')
            
            # Consultar Prolog
            consulta = f"rutina_segura(usuario_{edad}, rutina_{rutina_data.get('id', 0)})"
            resultados = list(self.engine.query(consulta))
            
            if resultados:
                return (True, "Rutina segura según evaluación médica")
            else:
                return (False, "Rutina requiere precauciones médicas")
        except Exception as e:
            logger.error(f"Error en evaluación Prolog: {e}")
            return (True, "Evaluación no disponible, usar con precaución")
    
    def determinar_intensidad_recomendada(self, usuario_data: Dict) -> str:
        """
        Determina la intensidad recomendada basada en el perfil del usuario.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Intensidad recomendada ('baja', 'media', 'alta')
        """
        if PROLOG_AVAILABLE and self.engine:
            return self._intensidad_con_prolog(usuario_data)
        else:
            return self.motor_alternativo.determinar_intensidad_recomendada(usuario_data)
    
    def _intensidad_con_prolog(self, usuario_data: Dict) -> str:
        """Determina intensidad usando Prolog real."""
        try:
            edad = usuario_data.get('edad', 30)
            consulta = f"intensidad_recomendada(usuario_{edad}, Intensidad)"
            resultados = list(self.engine.query(consulta))
            
            if resultados:
                return resultados[0]['Intensidad']
            return 'media'
        except Exception as e:
            logger.error(f"Error en Prolog: {e}")
            return 'media'
    
    def determinar_objetivo_prioritario(self, usuario_data: Dict) -> str:
        """
        Determina el objetivo prioritario basado en IMC y perfil.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Objetivo prioritario
        """
        if PROLOG_AVAILABLE and self.engine:
            return self._objetivo_con_prolog(usuario_data)
        else:
            return self.motor_alternativo.determinar_objetivo_prioritario(usuario_data)
    
    def _objetivo_con_prolog(self, usuario_data: Dict) -> str:
        """Determina objetivo usando Prolog real."""
        try:
            imc = usuario_data.get('imc', 25.0)
            consulta = f"objetivo_prioritario(usuario_{imc}, Objetivo)"
            resultados = list(self.engine.query(consulta))
            
            if resultados:
                return resultados[0]['Objetivo']
            return 'mantenimiento'
        except Exception as e:
            logger.error(f"Error en Prolog: {e}")
            return 'mantenimiento'
    
    def generar_explicacion_medica(self, usuario_data: Dict, rutina_data: Dict) -> str:
        """
        Genera una explicación médica de por qué se recomienda esta rutina.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            rutina_data: Diccionario con datos de la rutina
            
        Returns:
            Explicación médica detallada
        """
        if PROLOG_AVAILABLE and self.engine:
            return self._explicacion_con_prolog(usuario_data, rutina_data)
        else:
            return self.motor_alternativo.generar_explicacion_medica(usuario_data, rutina_data)
    
    def _explicacion_con_prolog(self, usuario_data: Dict, rutina_data: Dict) -> str:
        """Genera explicación usando Prolog real."""
        explicaciones = []
        
        # Verificar compatibilidad
        try:
            consulta = f"rutina_compatible(usuario, rutina_{rutina_data.get('id', 0)})"
            if list(self.engine.query(consulta)):
                explicaciones.append("✓ Rutina compatible con tu perfil")
        except:
            pass
        
        # Verificar precauciones
        try:
            consulta = f"requiere_precaucion(usuario, rutina_{rutina_data.get('id', 0)}, Precaucion)"
            resultados = list(self.engine.query(consulta))
            for resultado in resultados:
                explicaciones.append(f"⚠ {resultado['Precaucion']}")
        except:
            pass
        
        return '\n'.join(explicaciones) if explicaciones else "Rutina recomendada según evaluación médica"
    
    def evaluar_condiciones(self, usuario_data: Dict) -> Dict[str, Any]:
        """
        Evalúa todas las condiciones médicas del usuario.
        
        Args:
            usuario_data: Diccionario con datos del usuario
            
        Returns:
            Diccionario con evaluación completa
        """
        if PROLOG_AVAILABLE and self.engine:
            return self._evaluar_condiciones_prolog(usuario_data)
        else:
            return self.motor_alternativo.evaluar_condiciones(usuario_data)
    
    def _evaluar_condiciones_prolog(self, usuario_data: Dict) -> Dict[str, Any]:
        """Evalúa condiciones usando Prolog real."""
        evaluacion = {
            'intensidad_recomendada': self.determinar_intensidad_recomendada(usuario_data),
            'objetivo_prioritario': self.determinar_objetivo_prioritario(usuario_data),
            'precauciones': [],
            'es_seguro': True
        }
        
        # Agregar precauciones
        edad = usuario_data.get('edad', 30)
        imc = usuario_data.get('imc', 25.0)
        
        if edad > 60:
            evaluacion['precauciones'].append("Edad avanzada: se recomienda intensidad baja")
        if imc > 30:
            evaluacion['precauciones'].append("Obesidad: comenzar con rutinas de baja intensidad")
        
        return evaluacion


class MotorLogicoAlternativo:
    """
    Motor lógico alternativo implementado en Python puro.
    Se usa cuando pyswip no está disponible.
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

