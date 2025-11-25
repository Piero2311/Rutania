# 🔍 Diagnóstico: Por qué no funciona el Chatbot con Gemini API

## 📋 Resumen del Problema

El chatbot muestra el mensaje: *"Lo siento, el chatbot no está configurado en este momento..."*

Esto indica que el chatbot **no está disponible** por alguna de las siguientes razones.

---

## 🔴 Problema 1: API Key No Configurada (MÁS PROBABLE)

### Síntoma:
- El chatbot muestra: "Lo siento, el chatbot no está configurado..."
- No hay errores en los logs

### Causa:
La variable de entorno `GEMINI_API_KEY` **no está configurada** en Render.com.

### Verificación:
El código verifica en `chatbot.py` línea 26:
```python
self.api_key = os.environ.get('GEMINI_API_KEY', '')
```

Si `GEMINI_API_KEY` está vacía, el chatbot no se inicializa.

### Solución:
1. **Obtener API Key de Gemini:**
   - Ve a: https://makersuite.google.com/app/apikey
   - O: https://aistudio.google.com/app/apikey
   - Crea una nueva API key

2. **Configurar en Render.com:**
   - Ve a tu servicio en Render Dashboard
   - Settings → Environment Variables
   - Agrega:
     - **Key:** `GEMINI_API_KEY`
     - **Value:** `tu_api_key_aqui`
   - Guarda y redepleya

3. **Verificar:**
   - Después del despliegue, el chatbot debería funcionar

---

## 🔴 Problema 2: Modelo 'gemini-pro' Deprecado

### Síntoma:
- API Key configurada correctamente
- Error en logs: "Model not found" o similar
- El chatbot no responde

### Causa:
Google ha actualizado los nombres de modelos de Gemini. `gemini-pro` puede estar deprecado.

### Solución:
Actualizar el código para usar el modelo correcto:

```python
# En chatbot.py, línea 33, cambiar:
self.model = genai.GenerativeModel('gemini-pro')

# Por:
self.model = genai.GenerativeModel('gemini-1.5-flash')  # Más rápido
# O:
self.model = genai.GenerativeAI('gemini-1.5-pro')      # Más potente
```

---

## 🔴 Problema 3: Versión de google-generativeai Incompatible

### Síntoma:
- Error al importar: `ImportError` o errores de sintaxis
- El chatbot no se inicializa

### Causa:
La versión `google-generativeai==0.3.2` puede ser antigua o incompatible.

### Solución:
Actualizar a la versión más reciente:

```bash
# En requirements.txt, cambiar:
google-generativeai==0.3.2

# Por:
google-generativeai>=0.8.0
```

---

## 🔴 Problema 4: Método generate_content() Cambiado

### Síntoma:
- API Key configurada
- Modelo correcto
- Error: "AttributeError" o "TypeError" en `generate_content()`

### Causa:
La API de Gemini ha cambiado. El método `generate_content()` puede requerir parámetros diferentes.

### Solución:
Actualizar el código para usar la nueva API:

```python
# Método antiguo (puede no funcionar):
response = self.model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(...)
)

# Método nuevo (recomendado):
response = self.model.generate_content(
    prompt,
    generation_config={
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 1024,
    }
)
```

---

## 🔴 Problema 5: API Key Inválida o Sin Permisos

### Síntoma:
- API Key configurada
- Error: "API key not valid" o "Permission denied"

### Causa:
- API Key incorrecta
- API Key sin permisos para usar Gemini
- API Key revocada o expirada

### Solución:
1. Verificar que la API Key sea correcta
2. Asegurarse de que la API Key tenga permisos para Gemini API
3. Generar una nueva API Key si es necesario

---

## 🔴 Problema 6: Límites de Cuota de API

### Síntoma:
- Funciona ocasionalmente
- Error: "Quota exceeded" o "Rate limit exceeded"

### Causa:
La API Key gratuita de Gemini tiene límites de uso.

### Solución:
- Esperar a que se reinicie el límite
- Actualizar a un plan de pago si es necesario
- Implementar rate limiting en el código

---

## 🛠️ Cómo Diagnosticar el Problema

### Paso 1: Verificar si la API Key está configurada

Agrega esto temporalmente en `chatbot.py`:

```python
def __init__(self):
    self.api_key = os.environ.get('GEMINI_API_KEY', '')
    logger.info(f"GEMINI_API_KEY configurada: {bool(self.api_key)}")
    logger.info(f"GEMINI_API_KEY length: {len(self.api_key)}")
    # ...
```

Luego revisa los logs en Render.com para ver si la key está presente.

### Paso 2: Verificar si el modelo se inicializa

Agrega logging:

```python
if GEMINI_AVAILABLE and self.api_key:
    try:
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Modelo Gemini inicializado correctamente")
    except Exception as e:
        logger.error(f"Error configurando Gemini: {str(e)}", exc_info=True)
        self.model = None
```

### Paso 3: Verificar errores en la respuesta

El código ya tiene logging en línea 121, pero puedes mejorarlo:

```python
except Exception as e:
    logger.error(f"Error en chatbot: {str(e)}", exc_info=True)
    logger.error(f"Tipo de error: {type(e).__name__}")
    return {
        'response': f'Error: {str(e)}',  # Temporalmente mostrar el error
        'error': str(e)
    }
```

---

## ✅ Solución Recomendada (Actualizar Código)

Actualizar el código para usar la versión más reciente de la API:

```python
# 1. Actualizar requirements.txt
google-generativeai>=0.8.0

# 2. Actualizar chatbot.py
self.model = genai.GenerativeModel('gemini-1.5-flash')  # Modelo más reciente

# 3. Actualizar método generate_content
response = self.model.generate_content(
    prompt,
    generation_config={
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 1024,
    }
)
```

---

## 📝 Checklist de Verificación

- [ ] ¿Está `GEMINI_API_KEY` configurada en Render.com?
- [ ] ¿La API Key es válida y tiene permisos?
- [ ] ¿La versión de `google-generativeai` es compatible?
- [ ] ¿El nombre del modelo es correcto?
- [ ] ¿Hay errores en los logs de Render.com?
- [ ] ¿La API Key tiene cuota disponible?

---

## 🚀 Próximos Pasos

1. **Verificar logs en Render.com** para ver el error específico
2. **Configurar `GEMINI_API_KEY`** si no está configurada
3. **Actualizar el código** si el modelo está deprecado
4. **Probar localmente** con una API Key para verificar que funciona

---

## 💡 Alternativa: Chatbot sin Gemini

Si no quieres usar Gemini, puedes implementar un chatbot simple con respuestas predefinidas o usar otra API como OpenAI, Claude, etc.

