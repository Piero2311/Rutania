"""
Chatbot con API de Gemini para recomendaciones personalizadas.
"""
import os
import logging
from typing import Dict, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)
# Modelo por defecto de Gemini (se puede sobrescribir con GEMINI_MODEL_NAME)
DEFAULT_GEMINI_MODEL = os.environ.get("GEMINI_MODEL_NAME", "models/gemini-1.5-flash")


try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai no disponible, chatbot deshabilitado")


class ChatbotRutania:
    """
    Chatbot personalizado usando Gemini API para ayudar a los usuarios
    con recomendaciones y preguntas sobre rutinas de ejercicio.
    """
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        # Nombre del modelo que queremos usar (de env o por defecto)
        self.model_name = os.environ.get('GEMINI_MODEL_NAME', DEFAULT_GEMINI_MODEL)
        self.model = None
        self.conversation_history = {}
        
        # Logging para diagnóstico
        logger.info(f"GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        logger.info(f"GEMINI_API_KEY configurada: {bool(self.api_key)}")
        logger.info(f"GEMINI_MODEL_NAME: {self.model_name}")
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                
                # Lista de modelos a probar (ordenados por compatibilidad)
                modelos_a_probar: List[str] = []
                
                # 1) Modelo definido en variable de entorno, si existe
                if self.model_name:
                    modelos_a_probar.append(self.model_name)
                
                # 2) Otros modelos típicos a probar (por si el de env falla)
                modelos_a_probar.extend([
                    "models/gemini-1.5-flash",
                    "models/gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-1.5-pro",
                    "models/gemini-pro",
                    "gemini-pro",
                    "models/gemini-2.0-flash",
                    "gemini-2.0-flash",
                ])
                
                # Quitar duplicados manteniendo el orden
                modelos_unicos: List[str] = []
                for m in modelos_a_probar:
                    if m not in modelos_unicos:
                        modelos_unicos.append(m)
                modelos_a_probar = modelos_unicos
                
                # Intentar inicializar con cada modelo
                for modelo_nombre in modelos_a_probar:
                    try:
                        logger.info(f"Intentando inicializar modelo Gemini: {modelo_nombre}")
                        self.model = genai.GenerativeModel(modelo_nombre)
                        # Prueba rápida
                        test_response = self.model.generate_content(
                            "Prueba corta de Rutania.",
                            generation_config={
                                "max_output_tokens": 8,
                            },
                        )
                        logger.info(f"Modelo Gemini '{modelo_nombre}' inicializado y verificado correctamente")
                        self.model_name = modelo_nombre
                        break
                    except Exception as e:
                        error_msg = str(e)
                        logger.warning(f"Falló modelo '{modelo_nombre}': {error_msg}")
                        # Si es error 404 / model not found, probamos el siguiente
                        if "404" in error_msg or "not found" in error_msg.lower() or "model" in error_msg.lower():
                            continue
                        else:
                            # Incluso si es otro error, probamos con el siguiente
                            continue
                
                if self.model is None:
                    logger.error("No se pudo inicializar ningún modelo de Gemini disponible")
                    # Intentar listar modelos disponibles para debugging
                    try:
                        models = genai.list_models()
                        disponibles = [
                            m.name
                            for m in models
                            if hasattr(m, "supported_generation_methods")
                            and "generateContent" in m.supported_generation_methods
                        ]
                        logger.info(f"Modelos disponibles con generateContent: {disponibles}")
                    except Exception as e_list:
                        logger.warning(f"No se pudieron listar modelos: {e_list}")
            except Exception as e:
                logger.error(f"Error configurando Gemini: {str(e)}", exc_info=True)
                self.model = None
        else:
            if not GEMINI_AVAILABLE:
                logger.warning(
                    "google-generativeai no está disponible. Instala: pip install google-generativeai"
                )
            if not self.api_key:
                logger.warning(
                    "GEMINI_API_KEY no está configurada. Configúrala en las variables de entorno."
                )
                
    def is_available(self) -> bool:
        """Verifica si el chatbot está disponible."""
        return GEMINI_AVAILABLE and self.model is not None and bool(self.api_key)
    
    def get_system_prompt(self) -> str:
        """Retorna el prompt del sistema para el chatbot."""
        return """Eres un asistente virtual especializado en fitness y salud para Rutania, 
una plataforma de recomendación de rutinas deportivas personalizadas.

Tu rol es:
- Ayudar a los usuarios con preguntas sobre rutinas de ejercicio
- Proporcionar consejos de salud y fitness basados en ciencia
- Explicar recomendaciones de rutinas de manera clara y motivadora
- Responder preguntas sobre nutrición básica relacionada con ejercicio
- Ser empático, profesional y alentador

IMPORTANTE:
- Siempre recomienda consultar con un médico antes de comenzar cualquier rutina nueva
- No proporciones diagnósticos médicos
- Enfócate en recomendaciones generales de fitness
- Usa un tono amigable pero profesional
- Responde en español

Si no estás seguro de algo, admítelo y sugiere consultar con un profesional."""
    
    def get_response(self, user_message: str, user_id: Optional[str] = None, 
                    user_context: Optional[Dict] = None) -> Dict:
        """
        Obtiene una respuesta del chatbot.
        
        Args:
            user_message: Mensaje del usuario
            user_id: ID del usuario para mantener historial
            user_context: Contexto del usuario (perfil, rutina actual, etc.)
            
        Returns:
            Diccionario con la respuesta y metadata
        """
        if not self.is_available():
            return {
                'response': 'Lo siento, el chatbot no está configurado en este momento. Puedes hacer tus preguntas directamente en el formulario de recomendación o contactar con soporte si necesitas ayuda adicional.',
                'error': 'Chatbot no configurado',
                'success': False
            }
        
        try:
            # Construir prompt con contexto
            prompt = self._build_prompt(user_message, user_context)
            logger.debug(f"Prompt generado (longitud: {len(prompt)} caracteres)")
            
            # Generar respuesta - intentar múltiples métodos
            response = None
            error_ultimo = None
            
            # Método 1: API simple sin config (más compatible)
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 1024,
                    }
                )
                logger.debug("Respuesta generada con config simple")
            except (TypeError, AttributeError, ValueError) as e1:
                error_ultimo = e1
                logger.warning(f"Config simple falló: {str(e1)}, intentando sin config")
                
                # Método 2: Sin generation_config (más básico)
                try:
                    response = self.model.generate_content(prompt)
                    logger.debug("Respuesta generada sin generation_config")
                except Exception as e2:
                    error_ultimo = e2
                    logger.warning(f"Sin config también falló: {str(e2)}, intentando API antigua")
                    
                    # Método 3: API antigua con GenerationConfig (versión 0.3.x)
                    try:
                        if hasattr(genai, 'types') and hasattr(genai.types, 'GenerationConfig'):
                            response = self.model.generate_content(
                                prompt,
                                generation_config=genai.types.GenerationConfig(
                                    temperature=0.7,
                                    top_p=0.8,
                                    top_k=40,
                                    max_output_tokens=1024,
                                )
                            )
                            logger.debug("Respuesta generada con API antigua (GenerationConfig)")
                        else:
                            raise AttributeError("GenerationConfig no disponible")
                    except Exception as e3:
                        error_ultimo = e3
                        logger.error(f"Todos los métodos fallaron. Último error: {str(e3)}", exc_info=True)
                        raise e3
            
            if response is None:
                raise Exception(f"No se pudo generar respuesta. Último error: {str(error_ultimo)}")
            
            # Obtener texto de la respuesta - múltiples formatos posibles
            bot_response = None
            try:
                # Formato 1: response.text (más común en versiones nuevas)
                if hasattr(response, 'text'):
                    bot_response = response.text.strip()
                    logger.debug("Texto obtenido de response.text")
            except AttributeError:
                pass
            
            if not bot_response:
                try:
                    # Formato 2: response.candidates[0].content.parts[0].text
                    if hasattr(response, 'candidates') and response.candidates:
                        if hasattr(response.candidates[0], 'content'):
                            if hasattr(response.candidates[0].content, 'parts'):
                                if response.candidates[0].content.parts:
                                    bot_response = response.candidates[0].content.parts[0].text.strip()
                                    logger.debug("Texto obtenido de candidates[0].content.parts[0].text")
                except (AttributeError, IndexError, KeyError) as e:
                    logger.warning(f"Error extrayendo de candidates: {str(e)}")
            
            if not bot_response:
                try:
                    # Formato 3: response.parts[0].text
                    if hasattr(response, 'parts') and response.parts:
                        bot_response = response.parts[0].text.strip()
                        logger.debug("Texto obtenido de parts[0].text")
                except (AttributeError, IndexError) as e:
                    logger.warning(f"Error extrayendo de parts: {str(e)}")
            
            if not bot_response:
                # Formato 4: Convertir a string (último recurso)
                bot_response = str(response).strip()
                logger.warning(f"No se pudo extraer texto, usando str(response): {bot_response[:100]}")
            
            if not bot_response or len(bot_response) < 1:
                raise ValueError("Respuesta vacía o inválida de Gemini")
            
            # Guardar en historial
            if user_id:
                if user_id not in self.conversation_history:
                    self.conversation_history[user_id] = []
                self.conversation_history[user_id].append({
                    'user': user_message,
                    'bot': bot_response
                })
                # Limitar historial a últimas 10 interacciones
                if len(self.conversation_history[user_id]) > 10:
                    self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
            
            logger.info(f"Chatbot respondió exitosamente (longitud: {len(bot_response)} caracteres)")
            return {
                'response': bot_response,
                'success': True
            }
            
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            logger.error(f"Error en chatbot: {error_type}: {error_msg}", exc_info=True)
            
            # Mensajes más específicos según el tipo de error
            if 'API key' in error_msg or 'authentication' in error_msg.lower() or '401' in error_msg or '403' in error_msg:
                user_message = 'Error de autenticación con Gemini. Por favor, verifica que la API key sea correcta y tenga permisos.'
            elif 'quota' in error_msg.lower() or 'rate limit' in error_msg.lower() or '429' in error_msg:
                user_message = 'Se ha excedido el límite de uso de la API. Por favor, intenta más tarde.'
            elif 'model' in error_msg.lower() or 'not found' in error_msg.lower() or '404' in error_msg:
                user_message = 'El modelo de Gemini no está disponible. Por favor, contacta con soporte.'
            elif '500' in error_msg or 'internal' in error_msg.lower():
                user_message = 'Error temporal del servidor de Gemini. Por favor, intenta de nuevo en unos momentos.'
            elif 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                user_message = 'La solicitud tardó demasiado. Por favor, intenta con un mensaje más corto.'
            else:
                # En desarrollo, mostrar el error completo; en producción, mensaje genérico
                if settings.DEBUG:
                    user_message = f'Error: {error_type}: {error_msg}'
                else:
                    user_message = f'Error al procesar tu mensaje ({error_type}). Por favor, intenta de nuevo.'
            
            return {
                'response': user_message,
                'error': error_msg,
                'error_type': error_type,
                'success': False
            }
    
    def _build_prompt(self, user_message: str, user_context: Optional[Dict] = None) -> str:
        """Construye el prompt completo con contexto del usuario."""
        prompt = self.get_system_prompt()
        
        if user_context:
            context_info = []
            if user_context.get('edad'):
                context_info.append(f"Edad: {user_context['edad']} años")
            if user_context.get('nivel_experiencia'):
                context_info.append(f"Nivel: {user_context['nivel_experiencia']}")
            if user_context.get('objetivo'):
                context_info.append(f"Objetivo: {user_context['objetivo']}")
            if user_context.get('rutina_actual'):
                context_info.append(f"Rutina actual: {user_context['rutina_actual']}")
            
            if context_info:
                prompt += "\n\nContexto del usuario:\n" + "\n".join(context_info)
        
        prompt += f"\n\nUsuario: {user_message}\nAsistente:"
        
        # Limitar longitud del prompt (algunos modelos tienen límites)
        max_length = 8000  # Dejar margen para la respuesta
        if len(prompt) > max_length:
            logger.warning(f"Prompt muy largo ({len(prompt)} caracteres), truncando...")
            prompt = prompt[:max_length] + "..."
        
        return prompt
    
    def clear_history(self, user_id: str):
        """Limpia el historial de conversación de un usuario."""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Instancia global del chatbot
chatbot = ChatbotRutania()

