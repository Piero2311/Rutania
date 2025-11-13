class MotorReglasLogicas:
    """
    Motor de reglas lógicas personalizado que implementa el paradigma lógico.
    Simula el comportamiento de pyDatalog con un sistema de reglas de inferencia.
    """
    
    def __init__(self):
        self.hechos = []
        self.reglas = []
        self.inferencias = {}
    
    def agregar_hecho(self, hecho: str, valor: any):
        """
        Agrega un hecho a la base de conocimiento.
        
        Args:
            hecho: Nombre del hecho
            valor: Valor del hecho
        """
        self.hechos.append((hecho, valor))
    
    def agregar_regla(self, condicion: callable, conclusion: str, valor: any):
        """
        Agrega una regla lógica.
        
        Args:
            condicion: Función que evalúa la condición
            conclusion: Nombre de la conclusión
            valor: Valor si se cumple la condición
        """
        self.reglas.append((condicion, conclusion, valor))
    
    def inferir(self) -> dict:
        """
        Ejecuta el motor de inferencia aplicando todas las reglas.
        
        Returns:
            Diccionario con todas las inferencias
        """
        self.inferencias = {}
        
        for condicion, conclusion, valor in self.reglas:
            if condicion(dict(self.hechos)):
                self.inferencias[conclusion] = valor
        
        return self.inferencias
    
    def obtener(self, clave: str, default=None):
        """
        Obtiene una inferencia o hecho.
        
        Args:
            clave: Clave a buscar
            default: Valor por defecto
        
        Returns:
            Valor encontrado o default
        """
        return self.inferencias.get(clave, default)
    
    def limpiar(self):
        """Limpia todos los hechos, reglas e inferencias."""
        self.hechos = []
        self.reglas = []
        self.inferencias = {}


def determinar_nivel_usuario(edad: int, dias_disponibles: int, imc_clasificacion: str) -> str:
    """
    Regla lógica: Determina el nivel del usuario basado en múltiples factores.
    
    Reglas:
    - Si edad > 50 O días < 3 → principiante
    - Si IMC = obesidad → principiante
    - Si días >= 5 Y edad < 30 → avanzado
    - Sino → intermedio
    """
    motor = MotorReglasLogicas()
    
    motor.agregar_hecho('edad', edad)
    motor.agregar_hecho('dias_disponibles', dias_disponibles)
    motor.agregar_hecho('imc_clasificacion', imc_clasificacion)
    
    motor.agregar_regla(
        lambda h: h['edad'] > 50,
        'nivel',
        'principiante'
    )
    
    motor.agregar_regla(
        lambda h: h['dias_disponibles'] < 3,
        'nivel',
        'principiante'
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'obesidad',
        'nivel',
        'principiante'
    )
    
    motor.agregar_regla(
        lambda h: h['dias_disponibles'] >= 5 and h['edad'] < 30 and h['imc_clasificacion'] in ['normal', 'sobrepeso'],
        'nivel',
        'avanzado'
    )
    
    motor.agregar_regla(
        lambda h: 3 <= h['dias_disponibles'] < 5 and h['edad'] < 50 and h['imc_clasificacion'] != 'obesidad',
        'nivel',
        'intermedio'
    )
    
    resultados = motor.inferir()
    return resultados.get('nivel', 'intermedio')


def determinar_objetivo_recomendado(objetivo_usuario: str, imc_clasificacion: str) -> str:
    """
    Regla lógica: Determina el objetivo recomendado basado en IMC y preferencias.
    
    Reglas:
    - Si IMC = obesidad O sobrepeso → peso (prioridad)
    - Si IMC = bajo_peso → musculación
    - Si IMC = normal → respetar objetivo del usuario
    """
    motor = MotorReglasLogicas()
    
    motor.agregar_hecho('objetivo_usuario', objetivo_usuario)
    motor.agregar_hecho('imc_clasificacion', imc_clasificacion)
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] in ['obesidad', 'sobrepeso'],
        'objetivo',
        'peso'
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'bajo_peso',
        'objetivo',
        'musculacion'
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'normal',
        'objetivo',
        objetivo_usuario
    )
    
    resultados = motor.inferir()
    return resultados.get('objetivo', objetivo_usuario)


def determinar_intensidad_segura(edad: int, imc_clasificacion: str, nivel: str) -> str:
    """
    Regla lógica: Determina la intensidad segura del ejercicio.
    
    Reglas:
    - Si edad > 50 → intensidad baja
    - Si IMC = obesidad → intensidad baja
    - Si nivel = principiante → intensidad baja o media
    - Si nivel = avanzado Y edad < 40 → intensidad alta
    - Sino → intensidad media
    """
    motor = MotorReglasLogicas()
    
    motor.agregar_hecho('edad', edad)
    motor.agregar_hecho('imc_clasificacion', imc_clasificacion)
    motor.agregar_hecho('nivel', nivel)
    
    motor.agregar_regla(
        lambda h: h['edad'] > 50,
        'intensidad',
        'baja'
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'obesidad',
        'intensidad',
        'baja'
    )
    
    motor.agregar_regla(
        lambda h: h['nivel'] == 'principiante' and h['edad'] <= 50,
        'intensidad',
        'baja'
    )
    
    motor.agregar_regla(
        lambda h: h['nivel'] == 'avanzado' and h['edad'] < 40,
        'intensidad',
        'alta'
    )
    
    motor.agregar_regla(
        lambda h: h['nivel'] == 'intermedio' and h['edad'] < 50,
        'intensidad',
        'media'
    )
    
    resultados = motor.inferir()
    return resultados.get('intensidad', 'media')


def validar_seguridad_rutina(rutina: dict, usuario_data: dict) -> tuple:
    """
    Regla lógica: Valida si una rutina es segura para el usuario.
    
    Reglas de seguridad:
    - Si edad > 60 Y intensidad alta → NO SEGURO
    - Si IMC = obesidad Y días > 5 → NO SEGURO
    - Si principiante Y nivel avanzado → NO SEGURO
    - Sino → SEGURO
    
    Returns:
        Tupla (es_seguro, razón)
    """
    motor = MotorReglasLogicas()
    
    motor.agregar_hecho('edad', usuario_data.get('edad', 0))
    motor.agregar_hecho('rutina_intensidad', rutina['intensidad'])
    motor.agregar_hecho('imc_clasificacion', usuario_data.get('imc_clasificacion', 'normal'))
    motor.agregar_hecho('rutina_dias', rutina['dias_semana'])
    motor.agregar_hecho('nivel_usuario', usuario_data.get('nivel_recomendado', 'principiante'))
    motor.agregar_hecho('nivel_rutina', rutina['nivel'])
    
    motor.agregar_regla(
        lambda h: h['edad'] > 60 and h['rutina_intensidad'] == 'alta',
        'seguro',
        False
    )
    
    motor.agregar_regla(
        lambda h: h['edad'] > 60 and h['rutina_intensidad'] == 'alta',
        'razon',
        'Intensidad muy alta para tu edad'
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'obesidad' and h['rutina_dias'] > 5,
        'seguro',
        False
    )
    
    motor.agregar_regla(
        lambda h: h['imc_clasificacion'] == 'obesidad' and h['rutina_dias'] > 5,
        'razon',
        'Demasiados días de entrenamiento para comenzar'
    )
    
    motor.agregar_regla(
        lambda h: h['nivel_usuario'] == 'principiante' and h['nivel_rutina'] == 'avanzado',
        'seguro',
        False
    )
    
    motor.agregar_regla(
        lambda h: h['nivel_usuario'] == 'principiante' and h['nivel_rutina'] == 'avanzado',
        'razon',
        'Rutina demasiado avanzada para tu nivel actual'
    )
    
    resultados = motor.inferir()
    es_seguro = resultados.get('seguro', True)
    razon = resultados.get('razon', 'Rutina segura y adecuada') if not es_seguro else 'Rutina segura y adecuada'
    
    return (es_seguro, razon)


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
    
    motor = MotorReglasLogicas()
    motor.agregar_hecho('edad', usuario_data['edad'])
    motor.agregar_hecho('imc_clasificacion', usuario_data['imc_clasificacion'])
    motor.agregar_hecho('nivel', usuario_data['nivel_recomendado'])
    motor.agregar_hecho('objetivo', usuario_data['objetivo_recomendado'])
    motor.agregar_hecho('dias', usuario_data['dias_disponibles'])
    
    if rutina['nivel'] == usuario_data['nivel_recomendado']:
        explicaciones.append(f"✓ Nivel {rutina['nivel']} adecuado para tu experiencia")
    
    if rutina['objetivo'] == usuario_data['objetivo_recomendado']:
        explicaciones.append(f"✓ Alineada con tu objetivo de {rutina['objetivo']}")
    
    if rutina['dias_semana'] <= usuario_data['dias_disponibles']:
        explicaciones.append(f"✓ Compatible con tu disponibilidad de {usuario_data['dias_disponibles']} días")
    
    if usuario_data['edad'] > 50 and rutina['intensidad'] == 'baja':
        explicaciones.append("✓ Intensidad baja recomendada por tu edad")
    
    if usuario_data['imc_clasificacion'] in ['sobrepeso', 'obesidad'] and rutina['objetivo'] == 'peso':
        explicaciones.append("✓ Enfocada en pérdida de peso según tu IMC")
    
    return '\n'.join(explicaciones) if explicaciones else 'Rutina compatible con tu perfil'
