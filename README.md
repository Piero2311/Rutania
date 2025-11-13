# Sistema de Recomendación de Rutinas Deportivas Multiparadigma

Sistema inteligente de recomendación de rutinas deportivas implementado en Django que integra **tres paradigmas de programación**: Imperativo, Funcional y Lógico.

## 🎯 Características

- **Recomendaciones Personalizadas**: Rutinas adaptadas a edad, IMC, objetivos y disponibilidad
- **Análisis Científico**: Cálculo de IMC, nivel de intensidad segura y compatibilidad
- **Motor de Reglas Lógicas**: Sistema de inferencia para determinar rutinas seguras
- **Catálogo Completo**: Más de 10 rutinas profesionales diferentes
- **Interfaz Web Moderna**: Diseño responsive y profesional

## 📐 Arquitectura Multiparadigma

### 1. Paradigma IMPERATIVO (`views.py`)
- Control de flujo secuencial
- Gestión de requests/responses HTTP
- Validación imperativa de datos
- Coordinación entre módulos

### 2. Paradigma FUNCIONAL (`processor.py`)
- **Funciones puras**: `calcular_imc()`, `clasificar_imc()`, `calcular_compatibilidad()`
- **filter()**: Filtrar rutinas por nivel, objetivo, días
- **map()**: Transformar datos del usuario, calcular puntuaciones
- **sorted()**: Ordenar rutinas por compatibilidad
- **reduce()**: Generar estadísticas agregadas
- **Lambdas**: Operaciones inline

### 3. Paradigma LÓGICO (`logic_rules.py`)
- Motor de reglas personalizado (compatible Python 3.11)
- Reglas de inferencia:
  - `Si edad > 50 → intensidad_baja`
  - `Si IMC > 25 → objetivo_peso`
  - `Si días < 3 → nivel_principiante`
- Validación de seguridad basada en reglas
- Explicaciones lógicas de recomendaciones

## 🚀 Instalación

### Requisitos
- Python 3.11+
- pip

### Pasos

1. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

2. **Ejecutar migraciones**:
```bash
python manage.py migrate
```

3. **Iniciar servidor**:
```bash
python manage.py runserver 0.0.0.0:5000
```

4. **Abrir navegador**:
```
http://localhost:5000
```

## 📁 Estructura del Proyecto

```
PROYECTO_RUTINAS_DJANGO/
├── README.md
├── requirements.txt
├── manage.py
│
├── django_project/          # Configuración Django
│   ├── __init__.py
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # Router principal
│   └── wsgi.py
│
└── recommender/            # App principal
    ├── __init__.py
    ├── apps.py
    ├── admin.py
    │
    ├── datos.py            # Base de conocimiento (10 rutinas)
    ├── processor.py        # ✅ PARADIGMA FUNCIONAL
    ├── logic_rules.py      # ✅ PARADIGMA LÓGICO
    ├── views.py            # ✅ PARADIGMA IMPERATIVO
    ├── urls.py             # URLs de la app
    │
    ├── templates/recommender/
    │   ├── base.html
    │   ├── index.html      # Página principal
    │   ├── resultado.html  # Recomendación
    │   ├── rutinas.html    # Catálogo
    │   └── acerca.html     # About
    │
    └── static/
        ├── css/
        │   └── styles.css  # Estilos profesionales
        └── js/
            └── script.js   # Interactividad FAQ
```

## 🌐 Vistas Disponibles

### 1. Página Principal (`/`)
- Hero section con presentación
- Formulario de recomendación (edad, peso, altura, días, objetivo)
- Sección de beneficios (3 tarjetas)
- Testimonios simulados
- FAQ colapsable

### 2. Resultados (`/recomendar`)
- Rutina recomendada principal con compatibilidad
- Perfil del usuario (IMC, nivel, objetivo)
- Explicación basada en reglas lógicas
- Plan semanal detallado
- Rutinas alternativas
- Validación de seguridad

### 3. Catálogo (`/rutinas`)
- Grid con todas las rutinas
- Filtros por nivel y objetivo
- Estadísticas (duración promedio, días promedio)

### 4. Acerca de (`/acerca-de`)
- Descripción del proyecto
- Explicación técnica de los 3 paradigmas
- Flujo de integración
- Tecnologías utilizadas

## 🔬 Ejemplos de Paradigmas

### Paradigma Funcional (processor.py)
```python
# Función pura
def calcular_imc(peso: float, altura: float) -> float:
    return peso / (altura ** 2)

# filter()
rutinas_filtradas = filter(lambda r: r['nivel'] == nivel, rutinas)

# map()
puntuaciones = map(lambda r: calcular_compatibilidad(r, usuario), rutinas)

# sorted()
ordenadas = sorted(rutinas_puntuadas, key=lambda x: x[1], reverse=True)
```

### Paradigma Lógico (logic_rules.py)
```python
# Motor de reglas
motor.agregar_regla(
    lambda h: h['edad'] > 50,
    'intensidad',
    'baja'
)

motor.agregar_regla(
    lambda h: h['imc_clasificacion'] == 'obesidad',
    'nivel',
    'principiante'
)

resultados = motor.inferir()
```

### Paradigma Imperativo (views.py)
```python
def recomendar(request):
    # 1. Validación
    if request.method != 'POST':
        return render(request, 'index.html')
    
    # 2. Procesamiento funcional
    imc = processor.calcular_imc(peso, altura)
    
    # 3. Inferencia lógica
    nivel = logic_rules.determinar_nivel_usuario(edad, dias, imc)
    
    # 4. Selección
    rutina, puntuacion = processor.obtener_mejor_rutina(rutinas, usuario)
    
    # 5. Renderizado
    return render(request, 'resultado.html', context)
```

## 📊 Base de Conocimiento

10 rutinas profesionales que incluyen:
- **Niveles**: Principiante, Intermedio, Avanzado
- **Objetivos**: Pérdida de peso, Ganancia muscular, Mantenimiento
- **Intensidades**: Baja, Media, Alta
- **Frecuencias**: 3-6 días/semana
- **Duraciones**: 30-60 minutos/sesión

Ejemplos:
- Cardio Suave (principiante, mantenimiento, 3 días)
- Pérdida de Peso Intensiva (intermedio, peso, 5 días)
- Musculación Avanzada (avanzado, musculación, 5 días)
- Tonificación Femenina (intermedio, musculación, 4 días)
- CrossFit para Principiantes (principiante, musculación, 3 días)

## 🛠️ Tecnologías

- **Django 4.2.7** - Framework web
- **Python 3.11** - Lenguaje base
- **HTML5/CSS3** - Frontend moderno
- **JavaScript** - Interactividad cliente
- **Motor de reglas personalizado** - Paradigma lógico

## 🎓 Objetivo Académico

Este proyecto demuestra:
1. **Integración multiparadigma** en un sistema real
2. **Separación clara** de responsabilidades por paradigma
3. **Cooperación** entre paradigmas diferentes
4. **Aplicación práctica** de conceptos teóricos

## 📝 Licencia

Proyecto académico - 2025

## 👨‍💻 Autor

Sistema desarrollado para demostrar la integración de paradigmas de programación en Django.
