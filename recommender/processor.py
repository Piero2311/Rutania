from functools import reduce
from typing import List, Dict, Callable


def calcular_imc(peso: float, altura: float) -> float:
    """
    Función pura para calcular el Índice de Masa Corporal.
    
    Args:
        peso: Peso en kilogramos
        altura: Altura en metros
    
    Returns:
        IMC calculado
    """
    return peso / (altura ** 2)


def clasificar_imc(imc: float) -> str:
    """
    Función pura para clasificar el IMC.
    
    Args:
        imc: Índice de Masa Corporal
    
    Returns:
        Clasificación del IMC
    """
    if imc < 18.5:
        return 'bajo_peso'
    elif imc < 25:
        return 'normal'
    elif imc < 30:
        return 'sobrepeso'
    else:
        return 'obesidad'


def calcular_compatibilidad(rutina: Dict, usuario_data: Dict) -> float:
    """
    Función pura para calcular la compatibilidad entre una rutina y un usuario.
    
    Args:
        rutina: Diccionario con datos de la rutina
        usuario_data: Diccionario con datos procesados del usuario
    
    Returns:
        Puntuación de compatibilidad (0-100)
    """
    puntuacion = 0
    
    if rutina['nivel'] == usuario_data['nivel_recomendado']:
        puntuacion += 40
    
    if rutina['objetivo'] == usuario_data['objetivo_recomendado']:
        puntuacion += 30
    
    if rutina['dias_semana'] <= usuario_data['dias_disponibles']:
        puntuacion += 20
    else:
        puntuacion += max(0, 20 - (rutina['dias_semana'] - usuario_data['dias_disponibles']) * 5)
    
    if rutina['intensidad'] == usuario_data['intensidad_recomendada']:
        puntuacion += 10
    
    return min(100, puntuacion)


def filtrar_rutinas_por_objetivo(rutinas: List[Dict], objetivo: str) -> List[Dict]:
    """
    Función que usa filter() para filtrar rutinas por objetivo.
    
    Args:
        rutinas: Lista de rutinas
        objetivo: Objetivo deseado
    
    Returns:
        Lista de rutinas filtradas
    """
    return list(filter(lambda r: r['objetivo'] == objetivo, rutinas))


def filtrar_rutinas_por_nivel(rutinas: List[Dict], nivel: str) -> List[Dict]:
    """
    Función que usa filter() para filtrar rutinas por nivel.
    
    Args:
        rutinas: Lista de rutinas
        nivel: Nivel de dificultad
    
    Returns:
        Lista de rutinas filtradas
    """
    return list(filter(lambda r: r['nivel'] == nivel, rutinas))


def filtrar_rutinas_por_dias(rutinas: List[Dict], dias_max: int) -> List[Dict]:
    """
    Función que usa filter() para filtrar rutinas por días disponibles.
    
    Args:
        rutinas: Lista de rutinas
        dias_max: Días máximos disponibles
    
    Returns:
        Lista de rutinas filtradas
    """
    return list(filter(lambda r: r['dias_semana'] <= dias_max, rutinas))


def transformar_datos_usuario(datos_form: Dict) -> Dict:
    """
    Función que usa map() y operaciones funcionales para transformar datos del formulario.
    
    Args:
        datos_form: Datos del formulario
    
    Returns:
        Datos transformados y validados
    """
    transformaciones = {
        'edad': lambda x: int(x),
        'peso': lambda x: float(x),
        'altura': lambda x: float(x),
        'dias_disponibles': lambda x: int(x),
        'objetivo': lambda x: str(x).lower()
    }
    
    datos_transformados = {}
    for campo, transformacion in transformaciones.items():
        if campo in datos_form:
            datos_transformados[campo] = transformacion(datos_form[campo])
    
    return datos_transformados


def calcular_puntuaciones(rutinas: List[Dict], usuario_data: Dict) -> List[tuple]:
    """
    Función que usa map() para calcular puntuaciones de todas las rutinas.
    
    Args:
        rutinas: Lista de rutinas
        usuario_data: Datos del usuario
    
    Returns:
        Lista de tuplas (rutina, puntuación)
    """
    return list(map(
        lambda r: (r, calcular_compatibilidad(r, usuario_data)),
        rutinas
    ))


def ordenar_por_puntuacion(rutinas_puntuadas: List[tuple]) -> List[tuple]:
    """
    Función que usa sorted() para ordenar rutinas por puntuación.
    
    Args:
        rutinas_puntuadas: Lista de tuplas (rutina, puntuación)
    
    Returns:
        Lista ordenada de mayor a menor puntuación
    """
    return sorted(rutinas_puntuadas, key=lambda x: x[1], reverse=True)


def obtener_mejor_rutina(rutinas: List[Dict], usuario_data: Dict) -> tuple:
    """
    Función que combina operaciones funcionales para obtener la mejor rutina.
    
    Args:
        rutinas: Lista de rutinas
        usuario_data: Datos del usuario
    
    Returns:
        Tupla (rutina, puntuación) de la mejor opción
    """
    rutinas_puntuadas = calcular_puntuaciones(rutinas, usuario_data)
    rutinas_ordenadas = ordenar_por_puntuacion(rutinas_puntuadas)
    
    return rutinas_ordenadas[0] if rutinas_ordenadas else (None, 0)


def obtener_rutinas_alternativas(rutinas: List[Dict], usuario_data: Dict, excluir_id: int, limite: int = 3) -> List[tuple]:
    """
    Función que obtiene rutinas alternativas usando filter, map y sorted.
    
    Args:
        rutinas: Lista de rutinas
        usuario_data: Datos del usuario
        excluir_id: ID de la rutina a excluir
        limite: Número máximo de alternativas
    
    Returns:
        Lista de tuplas (rutina, puntuación) alternativas
    """
    rutinas_filtradas = list(filter(lambda r: r['id'] != excluir_id, rutinas))
    rutinas_puntuadas = calcular_puntuaciones(rutinas_filtradas, usuario_data)
    rutinas_ordenadas = ordenar_por_puntuacion(rutinas_puntuadas)
    
    return rutinas_ordenadas[:limite]


def calcular_calorias_estimadas(duracion_minutos: int, intensidad: str, peso: float) -> int:
    """
    Función pura para calcular calorías estimadas quemadas.
    
    Args:
        duracion_minutos: Duración del ejercicio
        intensidad: Nivel de intensidad
        peso: Peso del usuario
    
    Returns:
        Calorías estimadas
    """
    factores_intensidad = {
        'baja': 3.5,
        'media': 6.0,
        'alta': 8.5
    }
    
    factor = factores_intensidad.get(intensidad, 5.0)
    calorias_por_minuto = (factor * 3.5 * peso) / 200
    
    return int(calorias_por_minuto * duracion_minutos)


def aplicar_filtros_multiples(rutinas: List[Dict], filtros: List[Callable]) -> List[Dict]:
    """
    Función que usa reduce() para aplicar múltiples filtros en secuencia.
    
    Args:
        rutinas: Lista de rutinas
        filtros: Lista de funciones filtro
    
    Returns:
        Lista de rutinas después de aplicar todos los filtros
    """
    return reduce(lambda ruts, filtro: list(filter(filtro, ruts)), filtros, rutinas)


def generar_resumen_estadistico(rutinas: List[Dict]) -> Dict:
    """
    Función que usa map() y reduce() para generar estadísticas.
    
    Args:
        rutinas: Lista de rutinas
    
    Returns:
        Diccionario con estadísticas
    """
    if not rutinas:
        return {
            'total': 0,
            'duracion_promedio': 0,
            'dias_promedio': 0
        }
    
    total = len(rutinas)
    duraciones = list(map(lambda r: r['duracion_minutos'], rutinas))
    dias = list(map(lambda r: r['dias_semana'], rutinas))
    
    duracion_promedio = reduce(lambda a, b: a + b, duraciones) / total
    dias_promedio = reduce(lambda a, b: a + b, dias) / total
    
    return {
        'total': total,
        'duracion_promedio': round(duracion_promedio, 1),
        'dias_promedio': round(dias_promedio, 1)
    }
