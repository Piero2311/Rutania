# 🚀 Configuración de Neon.tech para SportRoutineAI

Esta guía te ayudará a configurar Neon.tech (PostgreSQL serverless) como base de datos para SportRoutineAI.

## 📋 Requisitos Previos

- Cuenta en [Neon.tech](https://neon.tech) (gratis)
- Proyecto Django configurado

## 🔧 Pasos de Configuración

### 1. Crear Proyecto en Neon.tech

1. Ve a [https://neon.tech](https://neon.tech) y crea una cuenta
2. Haz clic en **"Create a project"**
3. Elige un nombre para tu proyecto (ej: `sportroutineai`)
4. Selecciona la región más cercana a tu ubicación
5. Elige la versión de PostgreSQL (recomendado: 15 o superior)
6. Haz clic en **"Create project"**

### 2. Obtener Connection String

Una vez creado el proyecto:

1. En el dashboard de Neon, ve a la sección **"Connection Details"**
2. Verás dos opciones de conexión:
   - **Direct connection**: Para desarrollo y conexiones directas
   - **Connection pooling**: Para producción (recomendado)

3. Copia la **Connection String** (formato):
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### 3. Configurar en Django

#### Opción A: Usando archivo .env (Recomendado)

1. Crea un archivo `.env` en la raíz del proyecto:
   ```bash
   cp env.example .env
   ```

2. Edita el archivo `.env` y agrega tu connection string:
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. El archivo `.env` ya está configurado para ser ignorado por git (seguridad)

#### Opción B: Variables de Entorno del Sistema

En Windows (PowerShell):
```powershell
$env:DATABASE_URL="postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

En Linux/Mac:
```bash
export DATABASE_URL="postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

### 4. Ejecutar Migraciones

Una vez configurada la conexión:

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 5. Verificar Conexión

Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

Si todo está correcto, deberías ver:
```
System check identified no issues (0 silenced).
Django version X.X.X, using settings 'django_project.settings'
Starting development server at http://127.0.0.1:8000/
```

## 🔐 Connection Pooling (Recomendado para Producción)

Neon.tech ofrece **connection pooling** para mejorar el rendimiento en producción:

1. En el dashboard de Neon, ve a **"Connection Details"**
2. Selecciona la opción **"Connection pooling"**
3. Copia la URL del pooler (tiene `-pooler` en el hostname)
4. Usa esta URL en lugar de la conexión directa

Ejemplo:
```
postgresql://username:password@ep-xxx-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## 🌐 Despliegue en Producción

### Render.com con Neon.tech

1. En Render.com, crea un nuevo **Web Service**
2. En **Environment Variables**, agrega:
   - `DATABASE_URL`: Tu connection string de Neon.tech
   - `SECRET_KEY`: Genera una clave secreta
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Tu dominio de Render

3. Render usará automáticamente la configuración de `settings.py`

### Otras Plataformas

Para cualquier plataforma (Heroku, Railway, etc.):

1. Agrega la variable de entorno `DATABASE_URL` con tu connection string de Neon
2. El sistema detectará automáticamente la conexión PostgreSQL

## 🛠️ Troubleshooting

### Error: "could not connect to server"

- Verifica que la URL de conexión sea correcta
- Asegúrate de que `sslmode=require` esté en la URL
- Verifica que tu IP no esté bloqueada (Neon permite todas por defecto)

### Error: "password authentication failed"

- Verifica que la contraseña en la URL sea correcta
- Puedes resetear la contraseña desde el dashboard de Neon

### Error: "database does not exist"

- Neon crea automáticamente una base de datos llamada `neondb`
- Si usas otro nombre, asegúrate de crearlo desde el dashboard

### Timeout en conexiones

- Usa **Connection Pooling** para producción
- Aumenta `conn_max_age` en `settings.py` si es necesario

## 📊 Ventajas de Neon.tech

- ✅ **Gratis hasta 0.5 GB** de almacenamiento
- ✅ **Serverless**: Se escala automáticamente
- ✅ **Branching**: Crea branches de tu BD para testing
- ✅ **Time Travel**: Restaura a puntos anteriores
- ✅ **Connection Pooling**: Mejor rendimiento
- ✅ **Sin configuración de servidor**: Todo manejado por Neon

## 🔗 Recursos

- [Documentación de Neon.tech](https://neon.tech/docs)
- [Guía de Connection Pooling](https://neon.tech/docs/connect/connection-pooling)
- [Dashboard de Neon.tech](https://console.neon.tech)

## ✅ Checklist

- [ ] Cuenta creada en Neon.tech
- [ ] Proyecto creado en Neon
- [ ] Connection string copiado
- [ ] Variable `DATABASE_URL` configurada
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Servidor funcionando correctamente

¡Listo! Tu base de datos está configurada con Neon.tech 🎉

