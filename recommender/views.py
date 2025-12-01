from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .datos import RUTINAS
from . import processor
from . import logic_rules
from .forms import (
    FormularioRegistro,
    FormularioPerfilMedico,
    FormularioActualizarUsuario,
    FormularioSeguimiento
)
from .models import UsuarioPersonalizado, PerfilMedico, RecomendacionMedica, SeguimientoUsuario, Rutina, SeguimientoEjercicio
from .motor_recomendacion import motor_recomendacion
from .chatbot import chatbot
from django.http import JsonResponse
import json


def index(request: HttpRequest) -> HttpResponse:
    """
    Vista principal - PARADIGMA IMPERATIVO.
    
    Implementa flujo de control secuencial:
    1. Inicializa contexto
    2. Valida request method
    3. Prepara datos para template
    4. Retorna respuesta
    """
    context = {
        'titulo': 'Sistema de Recomendación de Rutinas Deportivas',
        'total_rutinas': len(RUTINAS)
    }
    
    return render(request, 'recommender/index.html', context)


def recomendar(request: HttpRequest) -> HttpResponse:
    """
    Vista de recomendación - PARADIGMA IMPERATIVO.
    
    Flujo imperativo que coordina los tres paradigmas:
    1. Validación de datos (imperativo)
    2. Procesamiento funcional (processor.py)
    3. Inferencia lógica (logic_rules.py)
    4. Selección de resultado
    5. Renderizado
    """
    if request.method != 'POST':
        return render(request, 'recommender/index.html', {
            'error': 'Método no permitido. Use POST.'
        })
    
    try:
        datos_raw = {
            'edad': request.POST.get('edad'),
            'peso': request.POST.get('peso'),
            'altura': request.POST.get('altura'),
            'dias_disponibles': request.POST.get('dias_disponibles'),
            'objetivo': request.POST.get('objetivo')
        }
        
        errores = []
        if not datos_raw['edad'] or int(datos_raw['edad']) < 15 or int(datos_raw['edad']) > 100:
            errores.append('La edad debe estar entre 15 y 100 años')
        if not datos_raw['peso'] or float(datos_raw['peso']) < 30 or float(datos_raw['peso']) > 300:
            errores.append('El peso debe estar entre 30 y 300 kg')
        if not datos_raw['altura'] or float(datos_raw['altura']) < 1.0 or float(datos_raw['altura']) > 2.5:
            errores.append('La altura debe estar entre 1.0 y 2.5 metros')
        if not datos_raw['dias_disponibles'] or int(datos_raw['dias_disponibles']) < 1 or int(datos_raw['dias_disponibles']) > 7:
            errores.append('Los días disponibles deben estar entre 1 y 7')
        if not datos_raw['objetivo'] or datos_raw['objetivo'] not in ['peso', 'musculacion', 'mantenimiento']:
            errores.append('Objetivo inválido')
        
        if errores:
            return render(request, 'recommender/index.html', {
                'errores': errores,
                'total_rutinas': len(RUTINAS)
            })
        
        datos_usuario = processor.transformar_datos_usuario(datos_raw)
        
        imc = processor.calcular_imc(datos_usuario['peso'], datos_usuario['altura'])
        imc_clasificacion = processor.clasificar_imc(imc)
        
        nivel_recomendado = logic_rules.determinar_nivel_usuario(
            datos_usuario['edad'],
            datos_usuario['dias_disponibles'],
            imc_clasificacion
        )
        
        objetivo_recomendado = logic_rules.determinar_objetivo_recomendado(
            datos_usuario['objetivo'],
            imc_clasificacion
        )
        
        intensidad_recomendada = logic_rules.determinar_intensidad_segura(
            datos_usuario['edad'],
            imc_clasificacion,
            nivel_recomendado
        )
        
        datos_usuario['imc'] = imc
        datos_usuario['imc_clasificacion'] = imc_clasificacion
        datos_usuario['nivel_recomendado'] = nivel_recomendado
        datos_usuario['objetivo_recomendado'] = objetivo_recomendado
        datos_usuario['intensidad_recomendada'] = intensidad_recomendada
        
        rutina_principal, puntuacion = processor.obtener_mejor_rutina(RUTINAS, datos_usuario)
        
        if not rutina_principal:
            return render(request, 'recommender/index.html', {
                'error': 'No se encontró ninguna rutina compatible',
                'total_rutinas': len(RUTINAS)
            })
        
        es_seguro, razon_seguridad = logic_rules.validar_seguridad_rutina(rutina_principal, datos_usuario)
        
        explicacion = logic_rules.generar_explicacion_recomendacion(datos_usuario, rutina_principal)
        
        rutinas_alternativas = processor.obtener_rutinas_alternativas(
            RUTINAS,
            datos_usuario,
            rutina_principal['id'],
            limite=3
        )
        
        calorias_estimadas = processor.calcular_calorias_estimadas(
            rutina_principal['duracion_minutos'],
            rutina_principal['intensidad'],
            datos_usuario['peso']
        )
        
        context = {
            'usuario': datos_usuario,
            'rutina': rutina_principal,
            'puntuacion': round(puntuacion, 1),
            'es_seguro': es_seguro,
            'razon_seguridad': razon_seguridad,
            'explicacion': explicacion,
            'alternativas': rutinas_alternativas,
            'calorias_estimadas': calorias_estimadas,
            'imc_texto': f"{imc:.1f}",
            'imc_clasificacion_texto': {
                'bajo_peso': 'Bajo Peso',
                'normal': 'Normal',
                'sobrepeso': 'Sobrepeso',
                'obesidad': 'Obesidad'
            }.get(imc_clasificacion, 'Normal')
        }
        
        return render(request, 'recommender/resultado.html', context)
        
    except ValueError as e:
        return render(request, 'recommender/index.html', {
            'error': f'Datos inválidos: {str(e)}',
            'total_rutinas': len(RUTINAS)
        })
    except Exception as e:
        return render(request, 'recommender/index.html', {
            'error': f'Error inesperado: {str(e)}',
            'total_rutinas': len(RUTINAS)
        })


def catalogo_rutinas(request: HttpRequest) -> HttpResponse:
    """
    Vista de catálogo - PARADIGMA IMPERATIVO con operaciones funcionales.
    
    Flujo imperativo:
    1. Obtener parámetros de filtro
    2. Aplicar filtros usando funciones puras
    3. Preparar contexto
    4. Renderizar
    """
    nivel_filtro = request.GET.get('nivel', '')
    objetivo_filtro = request.GET.get('objetivo', '')
    
    rutinas_filtradas = RUTINAS.copy()
    
    if nivel_filtro:
        rutinas_filtradas = processor.filtrar_rutinas_por_nivel(rutinas_filtradas, nivel_filtro)
    
    if objetivo_filtro:
        rutinas_filtradas = processor.filtrar_rutinas_por_objetivo(rutinas_filtradas, objetivo_filtro)
    
    estadisticas = processor.generar_resumen_estadistico(rutinas_filtradas)
    
    context = {
        'rutinas': rutinas_filtradas,
        'nivel_filtro': nivel_filtro,
        'objetivo_filtro': objetivo_filtro,
        'estadisticas': estadisticas,
        'total_rutinas': len(rutinas_filtradas)
    }
    
    return render(request, 'recommender/rutinas.html', context)


def acerca_de(request: HttpRequest) -> HttpResponse:
    """
    Vista informativa - PARADIGMA IMPERATIVO simple.
    
    Flujo directo:
    1. Preparar información
    2. Renderizar
    """
    context = {
        'titulo': 'Acerca del Proyecto',
        'descripcion': 'Sistema de recomendación multiparadigma'
    }
    
    return render(request, 'recommender/acerca.html', context)


# ==================== VISTAS DE AUTENTICACIÓN ====================

def registro(request: HttpRequest) -> HttpResponse:
    """
    Vista de registro de usuario - PARADIGMA IMPERATIVO.
    
    Flujo:
    1. Validar método HTTP
    2. Validar formulario
    3. Crear usuario y perfil médico
    4. Autenticar y redirigir
    """
    if request.user.is_authenticated:
        return redirect('recommender:dashboard')
    
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            try:
                with transaction.atomic():
                    usuario = formulario.save(commit=True)
                    # El formulario ya crea el perfil médico
                    messages.success(request, f'¡Registro exitoso! Bienvenido a Rutania, {usuario.username}.')
                    login(request, usuario)
                    return redirect('recommender:dashboard')
            except Exception as e:
                # Mostrar error específico al usuario
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error en registro: {str(e)}", exc_info=True)
                messages.error(request, f'Error al crear la cuenta: {str(e)}. Por favor, intenta de nuevo.')
        else:
            # Mostrar errores específicos del formulario
            error_messages = []
            for field, errors in formulario.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            if error_messages:
                messages.error(request, 'Por favor corrige los siguientes errores: ' + ' | '.join(error_messages))
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        formulario = FormularioRegistro()
    
    return render(request, 'recommender/registro.html', {'formulario': formulario})


def login_usuario(request: HttpRequest) -> HttpResponse:
    """
    Vista de login - PARADIGMA IMPERATIVO con validación de seguridad.
    """
    if request.user.is_authenticated:
        return redirect('recommender:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f'¡Bienvenido de nuevo, {usuario.username}!')
                next_url = request.GET.get('next', 'recommender:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor completa todos los campos.')
    
    return render(request, 'recommender/login.html')


@login_required
def logout_usuario(request: HttpRequest) -> HttpResponse:
    """
    Vista de logout - PARADIGMA IMPERATIVO.
    """
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('recommender:index')


# ==================== VISTAS DE DASHBOARD Y PERFIL ====================

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Dashboard personalizado - PARADIGMA IMPERATIVO.
    
    Coordina:
    1. Obtención de datos del usuario
    2. Generación de recomendación (motor híbrido)
    3. Cálculo de progreso (funcional)
    4. Renderizado de información
    """
    usuario = request.user
    
    # Obtener o crear perfil médico
    try:
        perfil_medico = usuario.perfil_medico
    except PerfilMedico.DoesNotExist:
        perfil_medico = PerfilMedico.objects.create(usuario=usuario)
        motor_recomendacion._actualizar_perfil_medico(usuario, perfil_medico)
    
    # Obtener recomendación actual
    recomendacion_actual = None
    try:
        recomendacion_actual = usuario.recomendaciones.filter(vigente=True).latest('fecha_recomendacion')
    except RecomendacionMedica.DoesNotExist:
        pass
    
    # Generar nueva recomendación si no existe
    if not recomendacion_actual:
        try:
            resultado = motor_recomendacion.generar_recomendacion_completa(usuario)
            if 'recomendacion' in resultado:
                recomendacion_actual = resultado['recomendacion']
        except Exception as e:
            messages.warning(request, f'No se pudo generar recomendación: {str(e)}')
    
    # Calcular progreso (paradigma funcional)
    progreso = motor_recomendacion.calcular_progreso_promedio(usuario)
    
    # Obtener seguimientos recientes
    seguimientos_recientes = usuario.seguimientos.all()[:5]
    
    context = {
        'usuario': usuario,
        'perfil_medico': perfil_medico,
        'recomendacion_actual': recomendacion_actual,
        'progreso': progreso,
        'seguimientos_recientes': seguimientos_recientes,
    }
    
    return render(request, 'recommender/dashboard.html', context)


@login_required
def generar_recomendacion(request: HttpRequest) -> HttpResponse:
    """
    Genera una nueva recomendación médica - PARADIGMA IMPERATIVO.
    Coordina el motor híbrido de recomendación.
    """
    usuario = request.user
    
    # Validar que el usuario tenga datos necesarios
    if not usuario.altura or not usuario.peso:
        messages.error(request, 'Por favor completa tu altura y peso en tu perfil antes de generar una recomendación.')
        return redirect('recommender:perfil')
    
    try:
        # Verificar que haya rutinas disponibles
        rutinas_disponibles = Rutina.objects.filter(activa=True).count()
        if rutinas_disponibles == 0:
            messages.error(request, 'No hay rutinas disponibles en el sistema. Por favor, contacta al administrador.')
            return redirect('recommender:dashboard')
        
        resultado = motor_recomendacion.generar_recomendacion_completa(usuario)
        
        if 'error' in resultado:
            messages.error(request, resultado['error'])
            if 'precauciones' in resultado and resultado['precauciones']:
                messages.warning(request, 'Precauciones: ' + ' | '.join(resultado['precauciones']))
            return redirect('recommender:dashboard')
        
        # Verificar que se generó la recomendación
        if 'recomendacion' not in resultado:
            messages.error(request, 'No se pudo generar la recomendación. Por favor, intenta de nuevo.')
            return redirect('recommender:dashboard')
        
        # Marcar recomendaciones anteriores como no vigentes
        usuario.recomendaciones.filter(vigente=True).update(vigente=False)
        
        # Marcar la nueva como vigente
        resultado['recomendacion'].vigente = True
        resultado['recomendacion'].save()
        
        messages.success(request, '¡Nueva recomendación generada exitosamente!')
        return redirect('recommender:dashboard')
        
    except ValueError as e:
        # Error de validación
        messages.error(request, f'Error de validación: {str(e)}')
        return redirect('recommender:perfil')
    except Exception as e:
        # Error general - loguear para debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al generar recomendación para usuario {usuario.id}: {str(e)}", exc_info=True)
        messages.error(request, f'Error al generar recomendación: {str(e)}. Por favor, verifica que todos tus datos estén completos.')
        return redirect('recommender:dashboard')


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    """
    Vista de perfil del usuario - PARADIGMA IMPERATIVO.
    """
    usuario = request.user
    
    try:
        perfil_medico = usuario.perfil_medico
    except PerfilMedico.DoesNotExist:
        perfil_medico = PerfilMedico.objects.create(usuario=usuario)
        motor_recomendacion._actualizar_perfil_medico(usuario, perfil_medico)
    
    if request.method == 'POST':
        formulario_usuario = FormularioActualizarUsuario(request.POST, instance=usuario)
        
        if formulario_usuario.is_valid():
            formulario_usuario.save()
            
            # Actualizar perfil médico con nuevos datos
            motor_recomendacion._actualizar_perfil_medico(usuario, perfil_medico)
            
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('recommender:perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        formulario_usuario = FormularioActualizarUsuario(instance=usuario)
    
    context = {
        'usuario': usuario,
        'perfil_medico': perfil_medico,
        'formulario_usuario': formulario_usuario,
    }
    
    return render(request, 'recommender/perfil.html', context)


@login_required
def seguimiento(request: HttpRequest) -> HttpResponse:
    """
    Vista para registrar seguimiento de progreso - PARADIGMA IMPERATIVO.
    """
    usuario = request.user
    
    if request.method == 'POST':
        formulario = FormularioSeguimiento(request.POST, usuario=usuario)
        if formulario.is_valid():
            seguimiento = formulario.save(commit=False, usuario=usuario)
            seguimiento.save()
            messages.success(request, 'Seguimiento registrado correctamente.')
            return redirect('recommender:dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        formulario = FormularioSeguimiento(usuario=usuario)
    
    # Obtener seguimientos históricos
    seguimientos = usuario.seguimientos.all().order_by('-fecha')
    
    context = {
        'formulario': formulario,
        'seguimientos': seguimientos,
    }
    
    return render(request, 'recommender/seguimiento.html', context)


@login_required
def historial_recomendaciones(request: HttpRequest) -> HttpResponse:
    """
    Vista de historial de recomendaciones - PARADIGMA IMPERATIVO.
    """
    usuario = request.user
    recomendaciones = usuario.recomendaciones.all().order_by('-fecha_recomendacion')
    
    context = {
        'recomendaciones': recomendaciones,
    }
    
    return render(request, 'recommender/historial_recomendaciones.html', context)


@login_required
def chatbot_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint para el chatbot - PARADIGMA IMPERATIVO.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        # Obtener contexto del usuario
        usuario = request.user
        edad = usuario.calcular_edad() if usuario.fecha_nacimiento else None
        user_context = {
            'edad': edad,
            'nivel_experiencia': usuario.nivel_experiencia if hasattr(usuario, 'nivel_experiencia') else None,
            'objetivo': usuario.objetivos if hasattr(usuario, 'objetivos') else None,
        }
        
        # Obtener rutina actual si existe
        try:
            recomendacion_actual = usuario.recomendaciones.filter(vigente=True).latest('fecha_recomendacion')
            if recomendacion_actual and recomendacion_actual.rutina_recomendada:
                user_context['rutina_actual'] = recomendacion_actual.rutina_recomendada.nombre
        except:
            pass
        
        # Obtener respuesta del chatbot
        user_id = str(usuario.id)
        
        try:
            response = chatbot.get_response(user_message, user_id=user_id, user_context=user_context)
            
            # Asegurar que siempre haya un campo 'success'
            if 'success' not in response:
                response['success'] = 'error' not in response
            
            # Logging para debugging (solo en desarrollo)
            import logging
            logger = logging.getLogger(__name__)
            if 'error' in response:
                logger.warning(f"Chatbot retornó error: {response.get('error')}")
            
            return JsonResponse(response)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en chatbot_api: {str(e)}", exc_info=True)
            return JsonResponse({
                'response': f'Error interno del servidor: {str(e)}',
                'error': str(e),
                'success': False
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


@login_required
def rutina_semanal(request: HttpRequest, rutina_id: int) -> HttpResponse:
    """
    Vista para mostrar y gestionar el seguimiento semanal de una rutina.
    """
    usuario = request.user
    
    try:
        rutina = Rutina.objects.get(id=rutina_id, activa=True)
    except Rutina.DoesNotExist:
        messages.error(request, 'Rutina no encontrada.')
        return redirect('recommender:dashboard')
    
    # Verificar que el usuario tenga esta rutina recomendada
    tiene_recomendacion = usuario.recomendaciones.filter(
        rutina_recomendada=rutina,
        vigente=True
    ).exists()
    
    if not tiene_recomendacion:
        messages.warning(request, 'No tienes esta rutina recomendada.')
        return redirect('recommender:dashboard')
    
    try:
        # Obtener o crear plan semanal
        plan_semanal = rutina.plan_semanal or {}
        if not plan_semanal:
            # Si no hay plan semanal, crear uno básico desde ejercicios
            dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            ejercicios = rutina.ejercicios if isinstance(rutina.ejercicios, list) else []
            for i, dia in enumerate(dias[:rutina.dias_semana]):
                plan_semanal[dia] = ejercicios if ejercicios else [f'Ejercicio {i+1}']
            rutina.plan_semanal = plan_semanal
            rutina.save()
        
        # Obtener seguimientos de la semana actual
        from datetime import datetime, timedelta
        hoy = datetime.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        seguimientos = SeguimientoEjercicio.objects.filter(
            usuario=usuario,
            rutina=rutina,
            fecha__gte=inicio_semana,
            fecha__lte=fin_semana
        )
        
        # Convertir seguimientos a diccionario por día
        seguimientos_dict = {}
        for seg in seguimientos:
            seguimientos_dict[seg.dia_semana] = seg
        
        # Calcular progreso semanal
        total_ejercicios_semana = sum(len(ejercicios) if isinstance(ejercicios, list) else 0 for ejercicios in plan_semanal.values())
        ejercicios_completados_semana = sum(
            len(seg.ejercicios_completados) if seg.ejercicios_completados else 0 for seg in seguimientos
        )
        progreso_semanal = round((ejercicios_completados_semana / total_ejercicios_semana * 100), 2) if total_ejercicios_semana > 0 else 0
        
        context = {
            'rutina': rutina,
            'plan_semanal': plan_semanal,
            'seguimientos': seguimientos_dict,
            'progreso_semanal': progreso_semanal,
            'ejercicios_completados_semana': ejercicios_completados_semana,
            'total_ejercicios_semana': total_ejercicios_semana,
            'inicio_semana': inicio_semana,
            'fin_semana': fin_semana,
        }
        
        return render(request, 'recommender/rutina_semanal.html', context)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en rutina_semanal: {str(e)}", exc_info=True)
        messages.error(request, f'Error al cargar el seguimiento semanal: {str(e)}')
        return redirect('recommender:dashboard')


@login_required
def marcar_ejercicio(request: HttpRequest) -> HttpResponse:
    """
    API endpoint para marcar ejercicios como completados.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        rutina_id = data.get('rutina_id')
        dia_semana = data.get('dia_semana')
        ejercicio = data.get('ejercicio')
        fecha = data.get('fecha')
        
        if not all([rutina_id, dia_semana, ejercicio, fecha]):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        usuario = request.user
        rutina = Rutina.objects.get(id=rutina_id, activa=True)
        
        # Obtener plan semanal
        plan_semanal = rutina.plan_semanal or {}
        ejercicios_dia = plan_semanal.get(dia_semana, [])
        
        # Obtener o crear seguimiento
        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        seguimiento, created = SeguimientoEjercicio.objects.get_or_create(
            usuario=usuario,
            rutina=rutina,
            fecha=fecha_obj,
            dia_semana=dia_semana,
            defaults={
                'ejercicios_totales': ejercicios_dia,
                'ejercicios_completados': []
            }
        )
        
        # Agregar o quitar ejercicio
        if ejercicio in seguimiento.ejercicios_completados:
            seguimiento.ejercicios_completados.remove(ejercicio)
        else:
            if ejercicio not in seguimiento.ejercicios_completados:
                seguimiento.ejercicios_completados.append(ejercicio)
        
        # Verificar si el día está completo
        seguimiento.completado = len(seguimiento.ejercicios_completados) == len(seguimiento.ejercicios_totales)
        seguimiento.save()
        
        progreso_dia = seguimiento.calcular_progreso_dia()
        
        # Calcular progreso semanal
        from datetime import timedelta
        hoy = datetime.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        
        seguimientos_semana = SeguimientoEjercicio.objects.filter(
            usuario=usuario,
            rutina=rutina,
            fecha__gte=inicio_semana,
            fecha__lte=fin_semana
        )
        
        total_ejercicios_semana = sum(len(ejercicios) for ejercicios in plan_semanal.values())
        ejercicios_completados_semana = sum(
            len(seg.ejercicios_completados) for seg in seguimientos_semana
        )
        progreso_semanal = round((ejercicios_completados_semana / total_ejercicios_semana * 100), 2) if total_ejercicios_semana > 0 else 0
        
        return JsonResponse({
            'success': True,
            'progreso_dia': progreso_dia,
            'progreso_semanal': progreso_semanal,
            'ejercicios_completados': len(seguimiento.ejercicios_completados),
            'ejercicios_totales': len(seguimiento.ejercicios_totales),
            'completado': seguimiento.completado
        })
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en marcar_ejercicio: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
