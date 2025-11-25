"""
Chatbot con API de Gemini para recomendaciones personalizadas.
"""
import os
import logging
from typing import Dict, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)

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
        self.model = None
        self.conversation_history = {}
        
        # Logging para diagnóstico
        logger.info(f"GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        logger.info(f"GEMINI_API_KEY configurada: {bool(self.api_key)}")
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Intentar con modelos más recientes primero
                modelos_a_probar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                for modelo_nombre in modelos_a_probar:
                    try:
                        self.model = genai.GenerativeModel(modelo_nombre)
                        logger.info(f"Modelo Gemini '{modelo_nombre}' inicializado correctamente")
                        break
                    except Exception as e:
                        logger.warning(f"No se pudo inicializar modelo '{modelo_nombre}': {str(e)}")
                        continue
                
                if self.model is None:
                    logger.error("No se pudo inicializar ningún modelo de Gemini")
            except Exception as e:
                logger.error(f"Error configurando Gemini: {str(e)}", exc_info=True)
                self.model = None
        else:
            if not GEMINI_AVAILABLE:
                logger.warning("google-generativeai no está disponible. Instala: pip install google-generativeai")
            if not self.api_key:
                logger.warning("GEMINI_API_KEY no está configurada. Configúrala en las variables de entorno.")
    
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
            
            # Obtener historial de conversación si existe
            history = self.conversation_history.get(user_id, [])
            
            # Generar respuesta
            try:
                # Intentar con la nueva API primero
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'top_p': 0.8,
                        'top_k': 40,
                        'max_output_tokens': 1024,
                    }
                )
            except (TypeError, AttributeError):
                # Fallback a la API antigua si la nueva no funciona
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.7,
                            top_p=0.8,
                            top_k=40,
                            max_output_tokens=1024,
                        )
                    )
                except Exception as e:
                    logger.error(f"Error con API antigua: {str(e)}", exc_info=True)
                    raise
            
            # Obtener texto de la respuesta
            try:
                bot_response = response.text.strip()
            except AttributeError:
                # Si response no tiene .text, intentar otras formas
                if hasattr(response, 'candidates') and response.candidates:
                    bot_response = response.candidates[0].content.parts[0].text.strip()
                else:
                    bot_response = str(response).strip()
            
            if not bot_response:
                raise ValueError("Respuesta vacía de Gemini")
            
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
            
            return {
                'response': bot_response,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error en chatbot: {str(e)}")
            return {
                'response': 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
                'error': str(e)
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
        
        return prompt
    
    def clear_history(self, user_id: str):
        """Limpia el historial de conversación de un usuario."""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Instancia global del chatbot
chatbot = ChatbotRutania()

