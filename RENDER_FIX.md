# 🔧 Solución para el Error de Despliegue en Render

## Problema
Render está usando Python 3.13.4 por defecto, pero `psycopg2-binary==2.9.7` no es compatible con Python 3.13.

## Soluciones Aplicadas

### 1. Actualización de psycopg2-binary
- ✅ Actualizado de `2.9.7` → `2.9.10` (compatible con Python 3.13)

### 2. Configuración de Python 3.11
- ✅ Agregado `PYTHON_VERSION=3.11.11` en variables de entorno
- ✅ Especificado `pythonVersion: "3.11"` en render.yaml
- ✅ Creado `runtime.txt` con `python-3.11.9`

## Si el problema persiste

### Opción A: Configurar manualmente en Render Dashboard
1. Ve a tu servicio en Render
2. Settings → Environment Variables
3. Agrega: `PYTHON_VERSION` = `3.11.11`
4. Guarda y redepleya

### Opción B: Usar psycopg (psycopg3) en lugar de psycopg2
Si `psycopg2-binary` sigue dando problemas, puedes cambiar a `psycopg`:

```txt
# En requirements.txt, reemplazar:
# psycopg2-binary==2.9.10
psycopg[binary]>=3.1.0
```

Y actualizar `settings.py`:
```python
# Cambiar de:
'ENGINE': 'django.db.backends.postgresql'

# A:
'ENGINE': 'django.db.backends.postgresql'  # (sigue siendo el mismo)
# psycopg3 es compatible con el mismo ENGINE
```

## Verificación
Después de hacer commit y push, Render debería:
1. Usar Python 3.11.11 (por PYTHON_VERSION)
2. Instalar psycopg2-binary 2.9.10 (compatible)
3. Completar el build exitosamente

