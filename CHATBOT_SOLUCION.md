# 🤖 Explicación: Por qué no funciona el Chatbot con Gemini API

## 🔍 Análisis del Problema

El chatbot puede no funcionar por **varias razones**. Aquí te explico cada una:

---

## ❌ Problema 1: API Key No Configurada (MÁS COMÚN - 90% de los casos)

### ¿Qué está pasando?

El código en `chatbot.py` línea 26 busca la variable de entorno:
```python
self.api_key = os.environ.get('GEMINI_API_KEY', '')
```

Si `GEMINI_API_KEY` **no está configurada** en Render.com, el valor será una cadena vacía `''`.

Luego, en línea 30, verifica:
```python
if GEMINI_AVAILABLE and self.api_key:  # Si api_key está vacía, esto es False
```

Si `self.api_key` está vacía, el modelo **nunca se inicializa**, por lo que `self.model` queda como `None`.

Finalmente, en línea 40:
```python
def is_available(self) -> bool:
    return GEMINI_AVAILABLE and self.model is not None and bool(self.api_key)
```

Si `self.model` es `None` o `self.api_key` está vacía, retorna `False`, y el chatbot muestra el mensaje de "no configurado".

### ✅ Solución:

1. **Obtener API Key:**
   - Ve a: https://aistudio.google.com/app/apikey
   - Crea una nueva API key
   - Copia la key (formato: `AIza...`)

2. **Configurar en Render.com:**
   - Dashboard de Render → Tu servicio "rutania"
   - Settings → Environment Variables
   - Click en "Add Environment Variable"
   - Key: `GEMINI_API_KEY`
   - Value: `tu_api_key_aqui`
   - Guardar

3. **Redepleyar:**
   - Render detectará el cambio automáticamente
   - O haz "Manual Deploy" → "Clear build cache & deploy"

---

## ❌ Problema 2: Modelo 'gemini-pro' Deprecado

### ¿Qué está pasando?

Google ha actualizado los modelos de Gemini. El modelo `gemini-pro` puede estar:
- Deprecado
- No disponible en tu región
- Requerir una API key diferente

### ✅ Solución:

He actualizado el código para probar modelos más recientes automáticamente:
- `gemini-1.5-flash` (más rápido, recomendado)
- `gemini-1.5-pro` (más potente)
- `gemini-pro` (fallback)

El código ahora intenta cada modelo hasta que uno funcione.

---

## ❌ Problema 3: Versión Antigua de google-generativeai

### ¿Qué está pasando?

La versión `google-generativeai==0.3.2` es **muy antigua** (de 2023). La API ha cambiado significativamente.

### Cambios en la API:

**Versión antigua (0.3.2):**
```python
genai.types.GenerationConfig(...)  # Clase específica
```

**Versión nueva (0.8.0+):**
```python
{'temperature': 0.7, ...}  # Diccionario simple
```

### ✅ Solución:

He actualizado `requirements.txt` a `google-generativeai>=0.8.0` y el código ahora soporta ambas versiones.

---

## ❌ Problema 4: Errores en la Respuesta de Gemini

### ¿Qué está pasando?

A veces Gemini retorna la respuesta en un formato diferente:
- `response.text` puede no existir
- La respuesta puede estar en `response.candidates[0].content.parts[0].text`

### ✅ Solución:

He actualizado el código para manejar múltiples formatos de respuesta automáticamente.

---

## 🔧 Cómo Verificar el Problema

### Opción 1: Ver Logs en Render.com

1. Ve a tu servicio en Render Dashboard
2. Click en "Logs"
3. Busca mensajes que contengan:
   - `"GEMINI_API_KEY configurada: False"` → Problema 1
   - `"Error configurando Gemini"` → Problema 2 o 3
   - `"Error en chatbot"` → Problema 4

### Opción 2: Agregar Diagnóstico Temporal

Puedes agregar esto temporalmente en `chatbot.py` para ver qué está pasando:

```python
def is_available(self) -> bool:
    disponible = GEMINI_AVAILABLE and self.model is not None and bool(self.api_key)
    logger.info(f"Chatbot disponible: {disponible}")
    logger.info(f"  - GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
    logger.info(f"  - model is not None: {self.model is not None}")
    logger.info(f"  - api_key existe: {bool(self.api_key)}")
    return disponible
```

---

## 📊 Flujo de Verificación del Chatbot

```
1. ¿google-generativeai está instalado?
   ├─ NO → GEMINI_AVAILABLE = False → Chatbot no disponible
   └─ SÍ → Continúa

2. ¿GEMINI_API_KEY está configurada?
   ├─ NO → self.api_key = '' → Chatbot no disponible
   └─ SÍ → Continúa

3. ¿Se puede inicializar el modelo?
   ├─ NO → self.model = None → Chatbot no disponible
   └─ SÍ → Continúa

4. ¿is_available() retorna True?
   ├─ NO → Muestra mensaje "no configurado"
   └─ SÍ → Chatbot funciona ✅
```

---

## 🎯 Resumen de Cambios Realizados

1. ✅ **Actualizado `requirements.txt`**: `google-generativeai>=0.8.0`
2. ✅ **Mejorado inicialización**: Prueba múltiples modelos automáticamente
3. ✅ **Mejorado manejo de respuestas**: Soporta múltiples formatos
4. ✅ **Agregado logging detallado**: Para diagnóstico
5. ✅ **Mejorado manejo de errores**: Más información en los logs

---

## 🚀 Próximos Pasos

1. **Configurar `GEMINI_API_KEY` en Render.com** (si no está configurada)
2. **Hacer commit y push** de los cambios
3. **Redepleyar en Render.com**
4. **Verificar logs** para ver si hay errores específicos
5. **Probar el chatbot** nuevamente

---

## 💡 Si Aún No Funciona

Revisa los **logs en Render.com** y busca:
- `"GEMINI_API_KEY configurada: False"` → Configura la API key
- `"Error configurando Gemini"` → Revisa el error específico
- `"Error en chatbot"` → Revisa el error de la API

Los logs ahora mostrarán información detallada sobre qué está fallando.

