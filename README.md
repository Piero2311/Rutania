# 🏋️ Rutania - Tu camino inteligente hacia una vida saludable

Sistema completo de recomendación deportiva y médica personalizada implementado en Django 4.2.7 que integra **tres paradigmas de programación**: Imperativo, Funcional y Lógico, con base de datos PostgreSQL y despliegue en Render.com.

## 🎯 Características Principales

- ✅ **Sistema de Autenticación Seguro**: Registro, login y gestión de usuarios personalizados
- ✅ **Perfil Médico Completo**: IMC, condiciones médicas, alergias, medicamentos, historial de lesiones
- ✅ **Motor de Recomendación Híbrido**: Integra los tres paradigmas para generar recomendaciones personalizadas
- ✅ **Paradigma Lógico con pydatalog**: Motor de inferencia lógica basado en Datalog
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
- **pydatalog**: Motor de inferencia lógica basado en Datalog
- Reglas de inferencia médica declarativas:
  - `nivel_usuario('principiante') <= (edad(X), X > 50)`
  - `objetivo_recomendado('peso') <= (imc_clasificacion(X), X.in_(['obesidad', 'sobrepeso']))`
  - `intensidad_segura('baja') <= (imc_clasificacion('obesidad'))`
- Validación de seguridad basada en reglas lógicas
- Fallback a implementación Python pura si pydatalog no está disponible
- Explicaciones médicas generadas lógicamente

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
    ├── logic_rules.py        # ✅ PARADIGMA LÓGICO (pydatalog)
    ├── prolog_engine.py      # ✅ PARADIGMA LÓGICO (Prolog - legacy)
    ├── chatbot.py            # 🤖 Chatbot con Gemini API
    ├── motor_recomendacion.py  # Motor híbrido multiparadigma
    ├── forms.py              # Formularios Django
    ├── admin.py              # Configuración admin
    │
    ├── templates/recommender/
    │   ├── base.html         # Template base con Tailwind CSS
    │   ├── index.html         # Página principal
    │   ├── registro.html      # Registro de usuarios
    │   ├── login.html         # Login
    │   ├── dashboard.html    # Dashboard personalizado
    │   ├── perfil.html        # Perfil del usuario
    │   ├── seguimiento.html   # Registro de seguimiento
    │   └── historial_recomendaciones.html
    │
    └── static/
        ├── css/
        └── js/
```

## 🗄️ Modelos de Base de Datos

### UsuarioPersonalizado
- Extiende `AbstractUser` de Django
- Campos: fecha_nacimiento, altura, peso, objetivos, nivel_experiencia, condiciones_medicas, etc.

### PerfilMedico
- Relación 1:1 con UsuarioPersonalizado
- Campos: IMC, clasificación_IMC, presión arterial, frecuencia cardíaca, alergias, medicamentos, historial de lesiones

### Rutina
- Rutinas deportivas estructuradas
- Campos: nombre, descripción, nivel, objetivo, ejercicios (JSON), duración, intensidad, calorías estimadas

### RecomendacionMedica
- Recomendaciones generadas por el motor
- Campos: usuario, rutina_recomendada, explicación_medica, precauciones, reglas_aplicadas (JSON), score_confianza

### SeguimientoUsuario
- Historial de progreso del usuario
- Campos: fecha, peso_actual, IMC_actual, rutina_realizada, satisfacción, comentarios

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
- `/historial-recomendaciones/` - Ver historial completo
- `/api/chatbot/` - API del chatbot (POST) - Asistente virtual con Gemini

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

### Paradigma Lógico (pydatalog)
```python
from pydatalog import pyDatalog

# Definir reglas lógicas
pyDatalog.load("""
    nivel_usuario('principiante') <= (edad(X), X > 50)
    nivel_usuario('principiante') <= (dias_disponibles(X), X < 3)
    nivel_usuario('avanzado') <= (dias_disponibles(X), X >= 5) & (edad(Y), Y < 30)
    objetivo_recomendado('peso') <= (imc_clasificacion(X), X.in_(['obesidad', 'sobrepeso']))
    intensidad_segura('baja') <= (edad(X), X > 50)
""")

# Agregar hechos
+ edad(55)
+ dias_disponibles(2)
+ imc_clasificacion('sobrepeso')

# Consultar
resultado = pyDatalog.ask('nivel_usuario(X)')
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
- **pydatalog 0.17.3** - Motor de inferencia lógica (paradigma lógico)
- **google-generativeai 0.3.2** - API de Gemini para chatbot
- **Pillow 11.0.0** - Procesamiento de imágenes
- **Tailwind CSS 3.3+** - Framework CSS utility-first
- **Alpine.js 3.x** - Framework JavaScript ligero
- **Heroicons** - Sistema de iconos
- **Whitenoise** - Servir archivos estáticos
- **Gunicorn** - Servidor WSGI
- **dj-database-url** - Configuración de BD

## 📊 Motor de Recomendación

El `MotorRecomendacion` integra los tres paradigmas:

1. **Análisis Médico (Lógico)**: Evalúa condiciones médicas con pydatalog
2. **Filtrado Funcional**: Filtra rutinas seguras usando funciones puras
3. **Cálculo de Compatibilidad (Funcional)**: Calcula scores usando map/sorted
4. **Coordinación Imperativa**: Orquesta todo el proceso en las vistas

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
- `GEMINI_API_KEY` - API Key de Gemini para el chatbot (opcional)
- `PYTHON_VERSION` - Versión de Python (3.11.11 recomendado)

## 📝 Licencia

Proyecto académico - 2025

## 👨‍💻 Autor

Sistema desarrollado para demostrar la integración de paradigmas de programación en Django con características profesionales y desplegable en producción.

**Rutania** - Tu camino inteligente hacia una vida saludable
