"""
Motor de reglas lógicas usando pydatalog para el paradigma lógico.
Implementa inferencia basada en hechos y reglas usando pydatalog.
"""
try:
    from pydatalog import pyDatalog
    PYDATALOG_AVAILABLE = True
except ImportError:
    PYDATALOG_AVAILABLE = False
    # Fallback a implementación simple si pydatalog no está disponible
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("pydatalog no disponible, usando implementación fallback")

from typing import Dict, Tuple, Any

if PYDATALOG_AVAILABLE:
    # Inicializar pydatalog
    pyDatalog.create_terms('edad, dias_disponibles, imc_clasificacion, objetivo_usuario, nivel_usuario, intensidad_segura, rutina_segura, rutina_intensidad, rutina_dias, rutina_nivel, usuario_nivel, usuario_edad, usuario_imc, objetivo_recomendado')


def determinar_nivel_usuario(edad: int, dias_disponibles: int, imc_clasificacion: str) -> str:
    """
    Determina el nivel del usuario usando pydatalog.
    
    Args:
        edad: Edad del usuario
        dias_disponibles: Días disponibles para entrenar
        imc_clasificacion: Clasificación del IMC
        
    Returns:
        Nivel del usuario: 'principiante', 'intermedio' o 'avanzado'
    """
    if not PYDATALOG_AVAILABLE:
        return _determinar_nivel_usuario_fallback(edad, dias_disponibles, imc_clasificacion)
    
    try:
        # Limpiar hechos previos
        pyDatalog.clear()
        
        # Definir reglas
        pyDatalog.load("""
            nivel_usuario('principiante') <= (edad(X), X > 50)
            nivel_usuario('principiante') <= (dias_disponibles(X), X < 3)
            nivel_usuario('principiante') <= (imc_clasificacion('obesidad'))
            nivel_usuario('avanzado') <= (dias_disponibles(X), X >= 5) & (edad(Y), Y < 30) & (imc_clasificacion(Z), Z.in_(['normal', 'sobrepeso']))
            nivel_usuario('intermedio') <= (dias_disponibles(X), X >= 3) & (X < 5) & (edad(Y), Y < 50) & (imc_clasificacion(Z), Z != 'obesidad')
        """)
        
        # Agregar hechos
        + edad(edad)
        + dias_disponibles(dias_disponibles)
        + imc_clasificacion(imc_clasificacion)
        
        # Consultar nivel
        resultado = pyDatalog.ask('nivel_usuario(X)')
        
        if resultado:
            nivel = list(resultado)[0][0]
            return nivel
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error en pydatalog, usando fallback: {str(e)}")
    
    return _determinar_nivel_usuario_fallback(edad, dias_disponibles, imc_clasificacion)


def _determinar_nivel_usuario_fallback(edad: int, dias_disponibles: int, imc_clasificacion: str) -> str:
    """Fallback si pydatalog no está disponible."""
    if edad > 50 or dias_disponibles < 3 or imc_clasificacion == 'obesidad':
        return 'principiante'
    elif dias_disponibles >= 5 and edad < 30 and imc_clasificacion in ['normal', 'sobrepeso']:
        return 'avanzado'
    else:
        return 'intermedio'


def determinar_objetivo_recomendado(objetivo_usuario: str, imc_clasificacion: str) -> str:
    """
    Determina el objetivo recomendado usando pydatalog.
    
    Args:
        objetivo_usuario: Objetivo del usuario
        imc_clasificacion: Clasificación del IMC
        
    Returns:
        Objetivo recomendado
    """
    if not PYDATALOG_AVAILABLE:
        return _determinar_objetivo_recomendado_fallback(objetivo_usuario, imc_clasificacion)
    
    try:
        pyDatalog.clear()
        pyDatalog.load("""
            objetivo_recomendado('peso') <= (imc_clasificacion(X), X.in_(['obesidad', 'sobrepeso']))
            objetivo_recomendado('musculacion') <= (imc_clasificacion('bajo_peso'))
            objetivo_recomendado(X) <= (imc_clasificacion('normal')) & (objetivo_usuario(X))
        """)
        
        + imc_clasificacion(imc_clasificacion)
        + objetivo_usuario(objetivo_usuario)
        
        resultado = pyDatalog.ask('objetivo_recomendado(X)')
        
        if resultado:
            objetivo = list(resultado)[0][0]
            return objetivo
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error en pydatalog, usando fallback: {str(e)}")
    
    return _determinar_objetivo_recomendado_fallback(objetivo_usuario, imc_clasificacion)


def _determinar_objetivo_recomendado_fallback(objetivo_usuario: str, imc_clasificacion: str) -> str:
    """Fallback si pydatalog no está disponible."""
    if imc_clasificacion in ['obesidad', 'sobrepeso']:
        return 'peso'
    elif imc_clasificacion == 'bajo_peso':
        return 'musculacion'
    else:
        return objetivo_usuario


def determinar_intensidad_segura(edad: int, imc_clasificacion: str, nivel: str) -> str:
    """
    Determina la intensidad segura usando pydatalog.
    
    Args:
        edad: Edad del usuario
        imc_clasificacion: Clasificación del IMC
        nivel: Nivel del usuario
        
    Returns:
        Intensidad segura: 'baja', 'media' o 'alta'
    """
    if not PYDATALOG_AVAILABLE:
        return _determinar_intensidad_segura_fallback(edad, imc_clasificacion, nivel)
    
    try:
        pyDatalog.clear()
        pyDatalog.load("""
            intensidad_segura('baja') <= (edad(X), X > 50)
            intensidad_segura('baja') <= (imc_clasificacion('obesidad'))
            intensidad_segura('baja') <= (nivel_usuario('principiante')) & (edad(X), X <= 50)
            intensidad_segura('alta') <= (nivel_usuario('avanzado')) & (edad(X), X < 40)
            intensidad_segura('media') <= (nivel_usuario('intermedio')) & (edad(X), X < 50)
        """)
        
        + edad(edad)
        + imc_clasificacion(imc_clasificacion)
        + nivel_usuario(nivel)
        
        resultado = pyDatalog.ask('intensidad_segura(X)')
        
        if resultado:
            intensidad = list(resultado)[0][0]
            return intensidad
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error en pydatalog, usando fallback: {str(e)}")
    
    return _determinar_intensidad_segura_fallback(edad, imc_clasificacion, nivel)


def _determinar_intensidad_segura_fallback(edad: int, imc_clasificacion: str, nivel: str) -> str:
    """Fallback si pydatalog no está disponible."""
    if edad > 50 or imc_clasificacion == 'obesidad' or (nivel == 'principiante' and edad <= 50):
        return 'baja'
    elif nivel == 'avanzado' and edad < 40:
        return 'alta'
    else:
        return 'media'


def validar_seguridad_rutina(rutina: dict, usuario_data: dict) -> Tuple[bool, str]:
    """
    Valida si una rutina es segura usando pydatalog.
    
    Args:
        rutina: Diccionario con datos de la rutina
        usuario_data: Diccionario con datos del usuario
        
    Returns:
        Tupla (es_seguro, razón)
    """
    edad = usuario_data.get('edad', 0)
    imc_clasificacion = usuario_data.get('imc_clasificacion', 'normal')
    nivel_usuario_val = usuario_data.get('nivel_recomendado', 'principiante')
    rutina_intensidad_val = rutina.get('intensidad', 'media')
    rutina_dias_val = rutina.get('dias_semana', 3)
    rutina_nivel_val = rutina.get('nivel', 'intermedio')
    
    # Validación directa (más simple y confiable)
    if edad > 60 and rutina_intensidad_val == 'alta':
        return (False, 'Intensidad muy alta para tu edad')
    if imc_clasificacion == 'obesidad' and rutina_dias_val > 5:
        return (False, 'Demasiados días de entrenamiento para comenzar')
    if nivel_usuario_val == 'principiante' and rutina_nivel_val == 'avanzado':
        return (False, 'Rutina demasiado avanzada para tu nivel actual')
    
    return (True, 'Rutina segura y adecuada')


def generar_explicacion_recomendacion(usuario_data: dict, rutina: dict) -> str:
    """
    Genera una explicación lógica de por qué se recomendó esta rutina.
    
    Args:
        usuario_data: Datos del usuario
        rutina: Rutina recomendada
        
    Returns:
        Explicación detallada
    """
    explicaciones = []
    
    if rutina.get('nivel') == usuario_data.get('nivel_recomendado'):
        explicaciones.append(f"✓ Nivel {rutina['nivel']} adecuado para tu experiencia")
    
    if rutina.get('objetivo') == usuario_data.get('objetivo_recomendado'):
        explicaciones.append(f"✓ Alineada con tu objetivo de {rutina['objetivo']}")
    
    if rutina.get('dias_semana', 0) <= usuario_data.get('dias_disponibles', 0):
        explicaciones.append(f"✓ Compatible con tu disponibilidad de {usuario_data['dias_disponibles']} días")
    
    if usuario_data.get('edad', 0) > 50 and rutina.get('intensidad') == 'baja':
        explicaciones.append("✓ Intensidad baja recomendada por tu edad")
    
    if usuario_data.get('imc_clasificacion') in ['sobrepeso', 'obesidad'] and rutina.get('objetivo') == 'peso':
        explicaciones.append("✓ Enfocada en pérdida de peso según tu IMC")
    
    return '\n'.join(explicaciones) if explicaciones else 'Rutina compatible con tu perfil'
