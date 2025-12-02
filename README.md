# 🏋️ Rutania - Tu camino inteligente hacia una vida saludable

Sistema completo de recomendación deportiva y médica personalizada implementado en Django 4.2.7 que integra **tres paradigmas de programación**: Imperativo, Funcional y Lógico, con base de datos PostgreSQL y despliegue en Render.com.

## 🎯 Características Principales

- ✅ **Sistema de Autenticación Seguro**: Registro, login y gestión de usuarios personalizados
- ✅ **Perfil Médico Completo**: IMC, condiciones médicas, alergias, medicamentos, historial de lesiones
- ✅ **Motor de Recomendación Híbrido**: Integra los tres paradigmas para generar recomendaciones personalizadas
- ✅ **Paradigma Lógico con pyDatalog**: Motor de inferencia lógica Datalog/Prolog en Python puro (compatible con Render)
- ✅ **Filtrado por Condiciones de Salud**: Sistema que excluye rutinas contraindicadas según condiciones médicas
- ✅ **Seguimiento Semanal de Ejercicios**: Sistema para marcar ejercicios completados día a día
- ✅ **Chatbot Inteligente**: Asistente virtual con API de Gemini para recomendaciones personalizadas
- ✅ **Dashboard Personalizado**: Seguimiento de progreso, historial de recomendaciones
- ✅ **Base de Datos PostgreSQL**: Configurado para Render.com
- ✅ **Interfaz Tailwind CSS**: Diseño moderno y responsive con paleta de colores premium

## 📐 Arquitectura Multiparadigma

### 1. Paradigma IMPERATIVO (`views.py`)
- Control de flujo secuencial en vistas Django
- Gestión de autenticación y sesiones
- Validación imperativa de datos
- Coordinación entre módulos funcional y lógico

### 2. Paradigma FUNCIONAL (`processor.py`, `motor_recomendacion.py`)
- **Funciones puras**: `calcular_imc()`, `clasificar_imc()`, `calcular_compatibilidad()`
- **filter()**: Filtrar rutinas por seguridad, nivel, objetivo
- **map()**: Transformar datos, calcular puntuaciones
- **sorted()**: Ordenar rutinas por compatibilidad
- **reduce()**: Calcular promedios y estadísticas

### 3. Paradigma LÓGICO (`logic_rules.py`, `prolog_engine.py`)
- **pyDatalog**: Motor de inferencia lógica Datalog/Prolog en Python puro
  - No requiere SWI-Prolog instalado (100% Python)
  - Compatible con despliegues en la nube (Render, Railway, etc.)
  - Sintaxis similar a Prolog
  - Estable y mantenida activamente
- **Reglas Declarativas**: Implementación de reglas médicas usando programación lógica
  - Determinación de nivel de usuario según edad, días disponibles e IMC
  - Determinación de objetivo recomendado según IMC y objetivos del usuario
  - Determinación de intensidad segura según edad, IMC y nivel
  - Validación de seguridad de rutinas basada en reglas lógicas
- **Motor Alternativo**: Implementación Python pura cuando pyDatalog no está disponible
- Filtrado por condiciones de salud: Excluye rutinas contraindicadas
- Explicaciones médicas generadas lógicamente
- Evaluación de precauciones y recomendaciones personalizadas

## 🚀 Instalación y Configuración

### Requisitos
- Python 3.11+
- PostgreSQL (Render.com) o SQLite (desarrollo)
- pip

### Instalación Local

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd Rutania
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**:

   **Opción A: SQLite (Desarrollo local)**
   ```bash
   # No necesitas configurar nada, se usa SQLite automáticamente
   # si DATABASE_URL está vacío
   ```

5. **Ejecutar migraciones**:
```bash
python manage.py migrate
```

6. **Crear superusuario**:
```bash
python manage.py createsuperuser
```

7. **Iniciar servidor**:
```bash
python manage.py runserver
```

8. **Abrir navegador**:
```
http://localhost:8000
```

### Despliegue en Render.com

1. **Conectar repositorio** a Render.com
2. **Crear servicio Web** usando `render.yaml`
3. **Crear base de datos PostgreSQL** (se configura automáticamente)
4. **Variables de entorno** se configuran automáticamente desde `render.yaml`
5. **Desplegar** - Render ejecutará `build.sh` automáticamente

## 📁 Estructura del Proyecto

```
Rutania/
├── README.md
├── requirements.txt
├── render.yaml              # Configuración Render.com
├── build.sh                  # Script de build para producción
├── manage.py
│
├── django_project/           # Configuración Django
│   ├── settings.py           # Config con PostgreSQL, seguridad, etc.
│   ├── urls.py
│   └── wsgi.py
│
└── recommender/              # App principal
    ├── models.py             # UsuarioPersonalizado, PerfilMedico, Rutina, etc.
    ├── views.py              # ✅ PARADIGMA IMPERATIVO
    ├── processor.py          # ✅ PARADIGMA FUNCIONAL
    ├── logic_rules.py        # ✅ PARADIGMA LÓGICO (reglas Python puras)
    ├── prolog_engine.py      # ✅ PARADIGMA LÓGICO (pyDatalog - Datalog/Prolog en Python puro)
    ├── chatbot.py            # 🤖 Chatbot con Gemini API
    ├── motor_recomendacion.py  # Motor híbrido multiparadigma
    ├── forms.py              # Formularios Django
    ├── admin.py              # Configuración admin
    ├── datos.py              # Datos iniciales de rutinas
    │
    ├── templates/recommender/
    │   ├── base.html         # Template base con Tailwind CSS
    │   ├── index.html         # Página principal
    │   ├── registro.html      # Registro de usuarios
    │   ├── login.html         # Login
    │   ├── dashboard.html    # Dashboard personalizado
    │   ├── perfil.html        # Perfil del usuario
    │   ├── seguimiento.html   # Registro de seguimiento
    │   ├── rutina_semanal.html # Seguimiento semanal de ejercicios
    │   ├── rutinas.html       # Catálogo de rutinas
    │   ├── resultado.html     # Resultado de recomendación
    │   └── historial_recomendaciones.html
    │
    └── static/
        ├── css/
        └── js/
```

## 🗄️ Modelos de Base de Datos

### UsuarioPersonalizado
- Extiende `AbstractUser` de Django
- Campos: fecha_nacimiento, altura, peso, objetivos, nivel_experiencia, condiciones_medicas, condiciones_salud (JSON), dias_entrenamiento, restricciones

### PerfilMedico
- Relación 1:1 con UsuarioPersonalizado
- Campos: IMC, clasificación_IMC, presión arterial, frecuencia cardíaca, alergias, medicamentos, historial de lesiones
- Se actualiza automáticamente cuando cambian peso/altura

### Rutina
- Rutinas deportivas estructuradas
- Campos: nombre, descripción, nivel, objetivo, ejercicios (JSON), duración, intensidad, calorías estimadas, condiciones_contraindicadas (JSON), plan_semanal (JSON)
- Soporta plan semanal estructurado por días

### RecomendacionMedica
- Recomendaciones generadas por el motor
- Campos: usuario, rutina_recomendada, explicación_medica, precauciones, reglas_aplicadas (JSON), score_confianza, vigente

### SeguimientoUsuario
- Historial de progreso del usuario
- Campos: fecha, peso_actual, IMC_actual, rutina_realizada, satisfacción, comentarios

### SeguimientoEjercicio
- Seguimiento diario de ejercicios completados
- Campos: usuario, rutina, fecha, dia_semana, ejercicios_completados (JSON), ejercicios_totales (JSON), completado, notas
- Permite marcar ejercicios completados día a día

## 🎨 Diseño con Tailwind CSS

### Paleta de Colores Premium

```css
--primary-emerald: #10B981    /* Acciones principales */
--deep-forest: #047857        /* Hover y elementos activos */
--mint-cream: #ECFDF5         /* Fondos claros */
--charcoal-black: #1F2937     /* Textos y headers */
--slate-gray: #374151         /* Elementos secundarios */
--accent-teal: #0D9488        /* Acentos especiales */
--gold-accents: #F59E0B       /* Elementos premium */
```

### Características de Diseño

- ✅ **Mobile-first**: Diseño responsive desde móvil
- ✅ **Componentes modernos**: Cards, formularios, navegación
- ✅ **Gradientes elegantes**: Efectos visuales premium
- ✅ **Iconos Heroicons**: Sistema de iconos consistente
- ✅ **Tipografía Inter**: Fuente moderna y legible

## 🔐 Seguridad

- Autenticación segura con validadores de contraseña
- Sesiones seguras (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- Protección XSS y CSRF
- HSTS en producción
- Rate limiting configurable

## 🌐 Vistas Disponibles

### Públicas
- `/` - Página principal con formulario de recomendación
- `/recomendar/` - Generar recomendación (sin autenticación)
- `/rutinas/` - Catálogo de rutinas
- `/acerca-de/` - Información del proyecto
- `/registro/` - Registro de nuevos usuarios
- `/login/` - Inicio de sesión

### Autenticadas (requieren login)
- `/dashboard/` - Dashboard personalizado
- `/perfil/` - Editar perfil y datos médicos
- `/generar-recomendacion/` - Generar nueva recomendación
- `/seguimiento/` - Registrar seguimiento de progreso
- `/rutina-semanal/<rutina_id>/` - Seguimiento semanal de ejercicios de una rutina
- `/historial-recomendaciones/` - Ver historial completo
- `/api/chatbot/` - API del chatbot (POST) - Asistente virtual con Gemini
- `/api/marcar-ejercicio/` - API para marcar ejercicios como completados (POST)

## 🔬 Ejemplos de Paradigmas

### Paradigma Funcional
```python
# Función pura
def calcular_imc(peso: float, altura: float) -> float:
    return peso / (altura ** 2)

# filter() para seguridad
rutinas_seguras = filter(lambda r: es_rutina_segura(r, perfil), rutinas)

# map() para puntuaciones
puntuaciones = map(lambda r: calcular_compatibilidad(r, usuario), rutinas)

# reduce() para promedios
promedio = reduce(lambda acc, s: acc + s.imc_actual, seguimientos, 0) / len(seguimientos)
```

### Paradigma Lógico (pyDatalog)
```python
from recommender import logic_rules
from recommender.prolog_engine import motor_prolog
from pyDatalog import pyDatalog

# Reglas lógicas en Python puro (logic_rules.py)
nivel = logic_rules.determinar_nivel_usuario(
    edad=55,
    dias_disponibles=2,
    imc_clasificacion='sobrepeso'
)  # Retorna 'principiante'

objetivo = logic_rules.determinar_objetivo_recomendado(
    objetivo_usuario='salud',
    imc_clasificacion='obesidad'
)  # Retorna 'peso'

# Motor pyDatalog (prolog_engine.py) - Datalog/Prolog en Python puro
# Reglas declarativas cargadas automáticamente:
# intensidad_recomendada(Edad, 'baja') <= (Edad > 60)
# objetivo_prioritario(IMC, 'peso') <= (IMC > 30)

usuario_data = {'edad': 55, 'imc': 30.5, 'nivel_experiencia': 'principiante'}
rutina_data = {'id': 1, 'intensidad': 'alta', 'dias_semana': 6}

# Evaluar seguridad usando reglas lógicas declarativas
es_seguro, razon = motor_prolog.evaluar_seguridad_rutina(
    usuario_data, rutina_data
)  # Retorna (False, "Intensidad alta no recomendada para mayores de 60 años")

# Consultar pyDatalog directamente
X = pyDatalog.Variable()
query = pyDatalog.ask('intensidad_recomendada(55, X)')
# Retorna intensidad recomendada según reglas lógicas

# Evaluar condiciones médicas
evaluacion = motor_prolog.evaluar_condiciones(usuario_data)
# Retorna dict con intensidad_recomendada, objetivo_prioritario, precauciones
```

### Paradigma Imperativo
```python
@login_required
def dashboard(request):
    # 1. Validar autenticación
    usuario = request.user
    
    # 2. Obtener datos
    perfil = usuario.perfil_medico
    
    # 3. Coordinar módulos
    resultado = motor_recomendacion.generar_recomendacion_completa(usuario)
    
    # 4. Renderizar
    return render(request, 'dashboard.html', context)
```

## 🛠️ Tecnologías

- **Django 4.2.7** - Framework web
- **PostgreSQL** - Base de datos (producción en Render.com)
- **SQLite** - Base de datos (desarrollo local)
- **pyDatalog 0.17.3** - Motor de inferencia lógica Datalog/Prolog en Python puro (compatible con Render)
- **google-generativeai >=0.8.0** - API de Gemini para chatbot
- **Pillow 11.0.0** - Procesamiento de imágenes
- **Tailwind CSS 3.3+** - Framework CSS utility-first
- **Alpine.js 3.x** - Framework JavaScript ligero
- **Heroicons** - Sistema de iconos
- **Whitenoise 6.5.0** - Servir archivos estáticos
- **Gunicorn 21.2.0** - Servidor WSGI
- **dj-database-url 1.3.0** - Configuración de BD
- **python-dotenv 1.0.0** - Gestión de variables de entorno

## 📊 Motor de Recomendación

El `MotorRecomendacion` integra los tres paradigmas:

1. **Análisis Médico (Lógico)**: Evalúa condiciones médicas con pyDatalog (Datalog/Prolog en Python puro)
   - Determina nivel recomendado, objetivo prioritario e intensidad segura
   - Genera precauciones médicas personalizadas
   - Valida seguridad de rutinas según perfil del usuario

2. **Filtrado Funcional**: Filtra rutinas seguras usando funciones puras
   - Filtra por condiciones de salud contraindicadas
   - Filtra por seguridad médica (edad, IMC, nivel)
   - Usa `filter()` para aplicar múltiples criterios

3. **Cálculo de Compatibilidad (Funcional)**: Calcula scores usando map/sorted
   - Calcula compatibilidad entre rutina y usuario (0-100)
   - Ordena rutinas por score de compatibilidad
   - Genera rutinas alternativas

4. **Coordinación Imperativa**: Orquesta todo el proceso en las vistas
   - Valida datos del usuario
   - Coordina módulos funcional y lógico
   - Genera recomendación final y la guarda en BD

## 🏥 Sistema de Condiciones de Salud

El sistema incluye un filtrado inteligente basado en condiciones de salud:

- **Condiciones Contraindicadas**: Cada rutina puede tener una lista de condiciones de salud que la contraindican
- **Filtrado Automático**: Las rutinas se filtran automáticamente según las condiciones del usuario
- **Seguridad Médica**: El motor evalúa la seguridad de cada rutina antes de recomendarla
- **Precauciones Personalizadas**: Se generan precauciones específicas según el perfil médico del usuario

### Ejemplo de Uso

```python
# El usuario tiene condiciones de salud
usuario.condiciones_salud = ['hipertension', 'diabetes']

# El motor automáticamente excluye rutinas contraindicadas
resultado = motor_recomendacion.generar_recomendacion_completa(usuario)
# Solo retorna rutinas seguras para hipertensión y diabetes
```

## 📅 Seguimiento Semanal de Ejercicios

El sistema permite hacer seguimiento detallado de los ejercicios completados:

- **Plan Semanal**: Cada rutina tiene un plan semanal estructurado por días
- **Marcado de Ejercicios**: Los usuarios pueden marcar ejercicios como completados día a día
- **Progreso Visual**: Se muestra el progreso diario y semanal
- **Historial Completo**: Se guarda el historial de todos los ejercicios completados

### Características

- Vista semanal de la rutina con todos los días
- Marcar/desmarcar ejercicios individuales
- Cálculo automático de progreso (porcentaje completado)
- Notas personalizadas por día de entrenamiento

## 🤖 Chatbot con Gemini

El sistema incluye un chatbot inteligente integrado que utiliza la API de Gemini para:

- Responder preguntas sobre rutinas de ejercicio
- Proporcionar consejos de salud y fitness
- Explicar recomendaciones de manera clara
- Ayudar con dudas sobre nutrición básica relacionada con ejercicio
- Mantener contexto del usuario (edad, nivel, objetivo, rutina actual)

### Configuración del Chatbot

1. Obtener API Key de Gemini: https://makersuite.google.com/app/apikey
2. Agregar variable de entorno:
   ```bash
   GEMINI_API_KEY=tu_api_key_aqui
   ```
3. El chatbot aparecerá automáticamente en la esquina inferior derecha

### Uso del Chatbot

- Click en el icono de chat (esquina inferior derecha)
- Escribe tu pregunta
- El chatbot responderá basándose en tu perfil y contexto
- Mantiene historial de las últimas 3 interacciones
- Respuestas breves y directas (máximo 3-4 frases)
- Siempre incluye recomendación de consultar con médico cuando es apropiado

### Modelos Soportados

El chatbot intenta usar automáticamente el mejor modelo disponible:
- `models/gemini-1.5-flash` (por defecto, rápido y eficiente)
- `models/gemini-1.5-pro` (más potente)
- `models/gemini-pro` (compatibilidad con versiones anteriores)

Puedes configurar el modelo con la variable de entorno `GEMINI_MODEL_NAME`.

## 🚀 Despliegue

### Render.com
- Configuración automática con `render.yaml`
- Base de datos PostgreSQL incluida
- Build automático con `build.sh`
- Variables de entorno configuradas

### Variables de Entorno
- `SECRET_KEY` - Clave secreta Django (generada automáticamente en Render)
- `DEBUG` - Modo debug (False en producción)
- `DATABASE_URL` - URL de conexión PostgreSQL (configurada automáticamente en Render)
- `ALLOWED_HOSTS` - Hosts permitidos (`.onrender.com` en producción)
- `CSRF_TRUSTED_ORIGINS` - Orígenes confiables para CSRF (ej: `https://tu-app.onrender.com`)
- `GEMINI_API_KEY` - API Key de Gemini para el chatbot (opcional)
- `GEMINI_MODEL_NAME` - Nombre del modelo de Gemini a usar (opcional, por defecto `models/gemini-1.5-flash`)
- `PYTHON_VERSION` - Versión de Python (3.11+ recomendado)

### Cargar Rutinas Iniciales

Después del despliegue, carga las rutinas iniciales:

```bash
python manage.py cargar_rutinas
```

Este comando carga rutinas desde `recommender/datos.py` a la base de datos.

## 🔄 Comandos de Gestión

### Cargar Rutinas Iniciales

```bash
python manage.py cargar_rutinas
```

Este comando carga las rutinas desde `recommender/datos.py` a la base de datos. Útil después de:
- Primera instalación
- Reset de base de datos
- Despliegue en producción

### Crear Superusuario

```bash
python manage.py createsuperuser
```

### Ejecutar Migraciones

```bash
python manage.py migrate
```

### Recopilar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

## 📝 Notas Técnicas

### Motor pyDatalog

- El sistema usa **pyDatalog**, una implementación de Datalog (subconjunto de Prolog) en Python puro
- **No requiere SWI-Prolog** ni ninguna dependencia externa
- **100% compatible con despliegues en la nube** (Render, Railway, Heroku, etc.)
- **Sintaxis similar a Prolog**: Usa reglas declarativas como `intensidad_recomendada(Edad, 'baja') <= (Edad > 60)`
- Implementa reglas médicas de forma declarativa usando programación lógica
- Si pyDatalog no está disponible, usa automáticamente un fallback en Python puro
- pyDatalog es estable, mantenida activamente y fácil de usar

### Base de Datos

- **Desarrollo**: SQLite (automático si `DATABASE_URL` no está configurada)
- **Producción**: PostgreSQL (configurada con `DATABASE_URL`)
- El sistema detecta automáticamente qué base de datos usar

### Chatbot

- Funciona sin API key (muestra mensaje de error amigable)
- Soporta múltiples modelos de Gemini con fallback automático
- Limita respuestas a 220 tokens para mantenerlas breves
- Mantiene historial de últimas 3 interacciones por usuario

## 📝 Licencia

Proyecto académico - 2025

## 👨‍💻 Autor

Sistema desarrollado para demostrar la integración de paradigmas de programación en Django con características profesionales y desplegable en producción.

**Rutania** - Tu camino inteligente hacia una vida saludable
