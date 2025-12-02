# 🚀 Guía Completa de Despliegue - Rutania

Esta guía te ayudará a desplegar Rutania en diferentes plataformas de hosting.

## 📋 Tabla de Contenidos

1. [Despliegue en Render.com](#rendercom)
2. [Render.com con Neon.tech](#rendercom-con-neontech)
3. [Railway](#railway)
4. [Heroku](#heroku)
5. [Vercel](#vercel)
6. [Configuración Manual](#configuración-manual)
7. [Troubleshooting](#troubleshooting)

---

## 🌐 Render.com

### Opción 1: Con Base de Datos de Render (Automático)

Render.com puede crear automáticamente una base de datos PostgreSQL para ti.

#### Pasos:

1. **Preparar el repositorio**
   - Asegúrate de que `render.yaml` esté en la raíz del proyecto
   - Sube tu código a GitHub/GitLab/Bitbucket

2. **Crear cuenta en Render.com**
   - Ve a [render.com](https://render.com)
   - Conecta tu cuenta de GitHub

3. **Desplegar desde render.yaml**
   - En el dashboard de Render, haz clic en **"New"** → **"Blueprint"**
   - Conecta tu repositorio
   - Render detectará automáticamente el archivo `render.yaml`
   - Haz clic en **"Apply"**

4. **Render hará automáticamente:**
   - ✅ Crear el servicio web
   - ✅ Crear la base de datos PostgreSQL
   - ✅ Configurar todas las variables de entorno
   - ✅ Ejecutar `build.sh`
   - ✅ Desplegar la aplicación

5. **Esperar el despliegue**
   - El primer despliegue puede tardar 5-10 minutos
   - Verás el progreso en el dashboard

6. **Crear superusuario**
   - Una vez desplegado, abre la consola de Render
   - Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

#### Variables de Entorno (Automáticas)

Render configura automáticamente:
- `DATABASE_URL` - Desde la base de datos creada
- `SECRET_KEY` - Generado automáticamente
- `DEBUG` - `False`
- `ALLOWED_HOSTS` - `.onrender.com`
- `CSRF_TRUSTED_ORIGINS` - `https://*.onrender.com`

---

### Opción 2: Render.com con Neon.tech (Recomendado)

Usar Neon.tech como base de datos externa es más flexible y gratuito.

#### Pasos:

1. **Configurar Neon.tech**
   - Sigue la guía en `NEON_SETUP.md`
   - Crea un proyecto y copia el connection string
   - **Usa Connection Pooling** para producción

2. **Crear servicio en Render**
   - Ve a [render.com](https://render.com)
   - Haz clic en **"New"** → **"Web Service"**
   - Conecta tu repositorio

3. **Configurar el servicio**
   - **Name**: `sportroutineai-medico`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT`

4. **Configurar Variables de Entorno**
   En la sección **"Environment Variables"**, agrega:

   ```
   DATABASE_URL=postgresql://user:pass@ep-xxx-pooler.neon.tech/db?sslmode=require
   SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui
   DEBUG=False
   ALLOWED_HOSTS=tu-app.onrender.com
   CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
   GEMINI_API_KEY=tu-api-key-de-gemini (opcional, para chatbot)
   GEMINI_MODEL_NAME=models/gemini-1.5-flash (opcional)
   ```

   **Generar SECRET_KEY:**
   ```python
   # En Python shell:
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

5. **Desplegar**
   - Haz clic en **"Create Web Service"**
   - Render ejecutará `build.sh` automáticamente

6. **Verificar despliegue**
   - Espera a que el build termine (5-10 min)
   - Visita tu URL: `https://tu-app.onrender.com`

7. **Cargar rutinas iniciales**
   - Una vez desplegado, ejecuta en la consola de Render:
   ```bash
   python manage.py cargar_rutinas
   ```
   - Esto carga las rutinas desde `recommender/datos.py` a la base de datos

---

## 🚂 Railway

Railway es otra excelente opción para desplegar Django.

### Pasos:

1. **Crear cuenta en Railway**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu cuenta de GitHub

2. **Crear nuevo proyecto**
   - Haz clic en **"New Project"**
   - Selecciona **"Deploy from GitHub repo"**
   - Elige tu repositorio

3. **Configurar servicio**
   - Railway detectará automáticamente que es un proyecto Python
   - Configura las variables de entorno:

   ```
   DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require
   SECRET_KEY=tu-clave-secreta
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   CSRF_TRUSTED_ORIGINS=https://*.railway.app
   GEMINI_API_KEY=tu-api-key-de-gemini (opcional)
   ```

4. **Agregar base de datos (opcional)**
   - Railway puede crear una PostgreSQL automáticamente
   - O usa Neon.tech como se muestra arriba

5. **Desplegar**
   - Railway detectará automáticamente `requirements.txt`
   - Ejecutará las migraciones si configuras un script de inicio

6. **Configurar dominio (opcional)**
   - En **Settings** → **Domains**
   - Agrega un dominio personalizado

---

## 🟣 Heroku

### Pasos:

1. **Instalar Heroku CLI**
   ```bash
   # Windows: descarga desde heroku.com
   # Mac: brew install heroku/brew/heroku
   # Linux: snap install heroku
   ```

2. **Login en Heroku**
   ```bash
   heroku login
   ```

3. **Crear aplicación**
   ```bash
   heroku create tu-app-name
   ```

4. **Agregar base de datos**
   ```bash
   # Opción A: PostgreSQL de Heroku (gratis con límites)
   heroku addons:create heroku-postgresql:mini
   
   # Opción B: Usar Neon.tech (recomendado)
   # Solo configura DATABASE_URL como variable de entorno
   ```

5. **Configurar variables de entorno**
   ```bash
   heroku config:set SECRET_KEY="tu-clave-secreta"
   heroku config:set DEBUG="False"
   heroku config:set ALLOWED_HOSTS="tu-app.herokuapp.com"
   heroku config:set CSRF_TRUSTED_ORIGINS="https://tu-app.herokuapp.com"
   
   # Si usas Neon.tech:
   heroku config:set DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require"
   
   # Opcional: Chatbot con Gemini
   heroku config:set GEMINI_API_KEY="tu-api-key"
   ```

6. **Crear Procfile**
   Crea un archivo `Procfile` en la raíz:
   ```
   web: gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT
   release: python manage.py migrate --noinput
   ```

7. **Desplegar**
   ```bash
   git push heroku main
   ```

8. **Crear superusuario y cargar rutinas**
   ```bash
   heroku run python manage.py createsuperuser
   heroku run python manage.py cargar_rutinas
   ```

---

## ▲ Vercel

Vercel es principalmente para frontend, pero puede desplegar Django con configuración especial.

### Pasos:

1. **Instalar Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Crear vercel.json**
   Crea `vercel.json` en la raíz:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "django_project/wsgi.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "django_project/wsgi.py"
       }
     ],
     "env": {
       "PYTHON_VERSION": "3.11"
     }
   }
   ```

3. **Desplegar**
   ```bash
   vercel
   ```

4. **Configurar variables de entorno**
   - En el dashboard de Vercel
   - Settings → Environment Variables

---

## 🔧 Configuración Manual

Si prefieres desplegar en tu propio servidor (VPS, AWS, DigitalOcean, etc.):

### Requisitos del Servidor

- Python 3.11+
- PostgreSQL o acceso a Neon.tech
- Nginx (recomendado)
- Supervisor o systemd (para gestionar Gunicorn)

### Pasos:

1. **Conectar al servidor**
   ```bash
   ssh usuario@tu-servidor.com
   ```

2. **Instalar dependencias del sistema**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql nginx
   ```

3. **Clonar repositorio**
   ```bash
   git clone https://github.com/tu-usuario/SportRoutineAI.git
   cd SportRoutineAI
   ```

4. **Crear entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configurar base de datos**
   ```bash
   # Configurar .env con DATABASE_URL
   cp env.example .env
   nano .env  # Editar con tus credenciales
   ```

6. **Ejecutar migraciones y cargar datos**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   python manage.py cargar_rutinas
   ```

7. **Configurar Gunicorn**
   Crea `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/ruta/a/SportRoutineAI
   ExecStart=/ruta/a/SportRoutineAI/venv/bin/gunicorn \
       --access-logfile - \
       --workers 3 \
       --bind unix:/ruta/a/SportRoutineAI/gunicorn.sock \
       django_project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

8. **Iniciar Gunicorn**
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

9. **Configurar Nginx**
   Crea `/etc/nginx/sites-available/sportroutineai`:
   ```nginx
   server {
       listen 80;
       server_name tu-dominio.com;

       location /static {
           alias /ruta/a/SportRoutineAI/staticfiles;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/ruta/a/SportRoutineAI/gunicorn.sock;
       }
   }
   ```

10. **Activar sitio**
    ```bash
    sudo ln -s /etc/nginx/sites-available/sportroutineai /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

---

## 🛠️ Troubleshooting

### Error: "No module named 'django'"

**Solución:**
- Verifica que todas las dependencias estén en `requirements.txt`
- Ejecuta `pip install -r requirements.txt` en el servidor

### Error: "Database connection failed"

**Solución:**
- Verifica que `DATABASE_URL` esté configurada correctamente
- Asegúrate de que `sslmode=require` esté en la URL
- Verifica que la IP del servidor no esté bloqueada (Neon permite todas por defecto)

### Error: "Static files not found"

**Solución:**
```bash
python manage.py collectstatic --noinput
```

### Error: "ALLOWED_HOSTS"

**Solución:**
- Agrega tu dominio a `ALLOWED_HOSTS` en variables de entorno
- Formato: `tu-dominio.com,www.tu-dominio.com`

### Error: "CSRF verification failed"

**Solución:**
- Agrega tu dominio a `CSRF_TRUSTED_ORIGINS`
- Formato: `https://tu-dominio.com`

### El sitio carga pero está en blanco

**Solución:**
- Revisa los logs del servidor
- En Render: Dashboard → Logs
- En Railway: Deployments → View Logs
- Verifica que las migraciones se ejecutaron correctamente

### Migraciones no se ejecutan automáticamente

**Solución:**
- Agrega al `build.sh` o `Procfile`:
  ```bash
  python manage.py migrate --noinput
  ```

---

## ✅ Checklist de Despliegue

Antes de desplegar, verifica:

- [ ] `requirements.txt` está actualizado
- [ ] `SECRET_KEY` está configurada (nunca en el código)
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` incluye tu dominio
- [ ] `CSRF_TRUSTED_ORIGINS` configurado
- [ ] `DATABASE_URL` configurada correctamente
- [ ] `GEMINI_API_KEY` configurada (opcional, para chatbot)
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recopilados (`collectstatic`)
- [ ] Rutinas iniciales cargadas (`cargar_rutinas`)
- [ ] Superusuario creado
- [ ] Logs verificados (sin errores críticos)

---

## 📊 Comparación de Plataformas

| Plataforma | Gratis | Base de Datos | Facilidad | Recomendado |
|------------|--------|---------------|-----------|-------------|
| **Render.com** | ✅ Sí | ✅ Incluida | ⭐⭐⭐⭐⭐ | ✅ Sí |
| **Railway** | ✅ Sí | ✅ Opcional | ⭐⭐⭐⭐ | ✅ Sí |
| **Heroku** | ⚠️ Limitado | ✅ Opcional | ⭐⭐⭐ | ⚠️ Medio |
| **Vercel** | ✅ Sí | ❌ Externa | ⭐⭐ | ❌ No |
| **VPS Manual** | ❌ No | Manual | ⭐⭐ | ⚠️ Avanzado |

---

## 🎯 Recomendación Final

**Para principiantes:** Render.com con Neon.tech
- Más fácil de configurar
- Gratis
- Documentación excelente

**Para producción:** Render.com o Railway
- Mejor rendimiento
- Escalabilidad
- Soporte confiable

---

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Documentación de Railway](https://docs.railway.app)
- [Documentación de Heroku](https://devcenter.heroku.com)
- [Guía de Neon.tech](NEON_SETUP.md)

---

¿Necesitas ayuda? Revisa los logs de despliegue o consulta la documentación de la plataforma elegida.

