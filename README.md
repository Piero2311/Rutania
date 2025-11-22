# 🏋️ Rutania - Tu camino inteligente hacia una vida saludable

Sistema completo de recomendación deportiva y médica personalizada implementado en Django 4.2.7 que integra **tres paradigmas de programación**: Imperativo, Funcional y Lógico, con base de datos PostgreSQL y despliegue en Render.com.

## 🎯 Características Principales

- ✅ **Sistema de Autenticación Seguro**: Registro, login y gestión de usuarios personalizados
- ✅ **Perfil Médico Completo**: IMC, condiciones médicas, alergias, medicamentos, historial de lesiones
- ✅ **Motor de Recomendación Híbrido**: Integra los tres paradigmas para generar recomendaciones personalizadas
- ✅ **Integración con Prolog**: Motor lógico para inferencia médica (con fallback a Python puro)
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

### 3. Paradigma LÓGICO (`prolog_engine.py`, `logic_rules.py`)
- Motor Prolog con `pyswip` (fallback a Python puro)
- Reglas de inferencia médica:
  - `Si edad > 60 → intensidad_baja`
  - `Si IMC > 30 → objetivo_peso`
  - `Si condiciones_médicas → rutina_segura`
- Validación de seguridad basada en reglas
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
    ├── prolog_engine.py      # ✅ PARADIGMA LÓGICO (Prolog)
    ├── logic_rules.py        # ✅ PARADIGMA LÓGICO (Python)
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

### Paradigma Lógico (Prolog)
```prolog
% Reglas de seguridad
rutina_segura(Usuario, Rutina) :-
    tiene_condicion(Usuario, Condicion),
    not contraindica_rutina(Rutina, Condicion).

intensidad_recomendada(Usuario, baja) :-
    edad(Usuario, Edad), Edad > 60.
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
- **PostgreSQL** - Base de datos (producción en Render)
- **SQLite** - Base de datos (desarrollo)
- **Prolog (pyswip)** - Motor lógico
- **Tailwind CSS** - Framework CSS utility-first
- **Alpine.js** - Framework JavaScript ligero
- **Whitenoise** - Servir archivos estáticos
- **Gunicorn** - Servidor WSGI
- **dj-database-url** - Configuración de BD

## 📊 Motor de Recomendación

El `MotorRecomendacion` integra los tres paradigmas:

1. **Análisis Médico (Lógico)**: Evalúa condiciones médicas con Prolog
2. **Filtrado Funcional**: Filtra rutinas seguras usando funciones puras
3. **Cálculo de Compatibilidad (Funcional)**: Calcula scores usando map/sorted
4. **Coordinación Imperativa**: Orquesta todo el proceso en las vistas

## 🚀 Despliegue

### Render.com
- Configuración automática con `render.yaml`
- Base de datos PostgreSQL incluida
- Build automático con `build.sh`
- Variables de entorno configuradas

### Variables de Entorno
- `SECRET_KEY` - Clave secreta Django
- `DEBUG` - Modo debug (False en producción)
- `DATABASE_URL` - URL de conexión PostgreSQL (Render)
- `ALLOWED_HOSTS` - Hosts permitidos

## 📝 Licencia

Proyecto académico - 2025

## 👨‍💻 Autor

Sistema desarrollado para demostrar la integración de paradigmas de programación en Django con características profesionales y desplegable en producción.

**Rutania** - Tu camino inteligente hacia una vida saludable
