# 🏋️ SportRoutineAI - Sistema Avanzado de Recomendación Deportiva y Médica

Sistema completo de recomendación deportiva y médica personalizada implementado en Django 4.2.7 que integra **tres paradigmas de programación**: Imperativo, Funcional y Lógico, con base de datos PostgreSQL y despliegue en Render.com.

## 🎯 Características Principales

- ✅ **Sistema de Autenticación Seguro**: Registro, login y gestión de usuarios personalizados
- ✅ **Perfil Médico Completo**: IMC, condiciones médicas, alergias, medicamentos, historial de lesiones
- ✅ **Motor de Recomendación Híbrido**: Integra los tres paradigmas para generar recomendaciones personalizadas
- ✅ **Integración con Prolog**: Motor lógico para inferencia médica (con fallback a Python puro)
- ✅ **Dashboard Personalizado**: Seguimiento de progreso, historial de recomendaciones
- ✅ **Base de Datos PostgreSQL**: Configurado para Neon.tech (serverless) o Render.com
- ✅ **SQLite para Desarrollo**: Fallback automático si no hay DATABASE_URL
- ✅ **Despliegue en Render.com**: Configuración completa incluida
- ✅ **Interfaz Bootstrap 5**: Diseño moderno y responsive

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
- PostgreSQL (Neon.tech recomendado) o SQLite (desarrollo)
- pip

### Instalación Local

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd SportRoutineAI
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

   **Opción A: Neon.tech (Recomendado - PostgreSQL serverless gratuito)**
   ```bash
   # Ver guía completa en NEON_SETUP.md
   # 1. Crear cuenta en https://neon.tech
   # 2. Crear proyecto y copiar connection string
   # 3. Configurar en .env:
   cp env.example .env
   # Editar .env y agregar: DATABASE_URL=postgresql://...
   ```

   **Opción B: SQLite (Desarrollo local)**
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
SportRoutineAI/
├── README.md
├── requirements.txt
├── render.yaml              # Configuración Render.com
├── build.sh                # Script de build para producción
├── manage.py
│
├── django_project/         # Configuración Django
│   ├── settings.py         # Config con PostgreSQL, seguridad, etc.
│   ├── urls.py
│   └── wsgi.py
│
└── recommender/            # App principal
    ├── models.py           # UsuarioPersonalizado, PerfilMedico, Rutina, etc.
    ├── views.py            # ✅ PARADIGMA IMPERATIVO
    ├── processor.py        # ✅ PARADIGMA FUNCIONAL
    ├── prolog_engine.py    # ✅ PARADIGMA LÓGICO (Prolog)
    ├── logic_rules.py      # ✅ PARADIGMA LÓGICO (Python)
    ├── motor_recomendacion.py  # Motor híbrido multiparadigma
    ├── forms.py            # Formularios Django
    ├── admin.py            # Configuración admin
    │
    ├── templates/recommender/
    │   ├── base.html       # Template base con Bootstrap 5
    │   ├── index.html      # Página principal
    │   ├── registro.html    # Registro de usuarios
    │   ├── login.html       # Login
    │   ├── dashboard.html   # Dashboard personalizado
    │   ├── perfil.html      # Perfil del usuario
    │   ├── seguimiento.html # Registro de seguimiento
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

## 🔐 Seguridad

- Autenticación segura con validadores de contraseña
- Sesiones seguras (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- Protección XSS y CSRF
- HSTS en producción
- Rate limiting (configurable con django-axes)

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
- **PostgreSQL** - Base de datos (producción)
- **SQLite** - Base de datos (desarrollo)
- **Prolog (pyswip)** - Motor lógico
- **Bootstrap 5** - Frontend framework
- **Whitenoise** - Servir archivos estáticos
- **Gunicorn** - Servidor WSGI
- **dj-database-url** - Configuración de BD
- **django-crispy-forms** - Formularios Bootstrap

## 📊 Motor de Recomendación

El `MotorRecomendacion` integra los tres paradigmas:

1. **Análisis Médico (Lógico)**: Evalúa condiciones médicas con Prolog
2. **Filtrado Funcional**: Filtra rutinas seguras usando funciones puras
3. **Cálculo de Compatibilidad (Funcional)**: Calcula scores usando map/sorted
4. **Coordinación Imperativa**: Orquesta todo el proceso en las vistas

## 🚀 Despliegue

### 📖 Guía Completa de Despliegue

**Consulta la guía completa en [`DEPLOYMENT.md`](DEPLOYMENT.md)** que incluye:
- ✅ Render.com (con base de datos propia o Neon.tech)
- ✅ Railway
- ✅ Heroku
- ✅ Vercel
- ✅ Despliegue manual en VPS
- ✅ Troubleshooting completo

### Opciones Rápidas

#### 🟢 Render.com (Más Fácil)
1. Conecta tu repositorio a Render
2. Usa el archivo `render.yaml` (despliegue automático)
3. O crea servicio manual y configura variables de entorno

#### 🟡 Render.com + Neon.tech (Recomendado)
1. Configura Neon.tech (ver `NEON_SETUP.md`)
2. Crea servicio en Render
3. Agrega `DATABASE_URL` de Neon como variable de entorno
4. Despliega

#### 🔵 Railway
1. Conecta repositorio
2. Configura variables de entorno
3. Despliega automáticamente

### Variables de Entorno Necesarias

```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
SECRET_KEY=tu-clave-secreta-muy-larga
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com
```

### Guías Específicas

- 📘 **Despliegue completo**: [`DEPLOYMENT.md`](DEPLOYMENT.md)
- 🗄️ **Configuración Neon.tech**: [`NEON_SETUP.md`](NEON_SETUP.md)

## 📝 Licencia

Proyecto académico - 2025

## 👨‍💻 Autor

Sistema desarrollado para demostrar la integración de paradigmas de programación en Django con características profesionales y desplegable en producción.
