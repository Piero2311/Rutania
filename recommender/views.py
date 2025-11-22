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
from .models import UsuarioPersonalizado, PerfilMedico, RecomendacionMedica, SeguimientoUsuario
from .motor_recomendacion import motor_recomendacion


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
        return redirect('dashboard')
    
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            with transaction.atomic():
                usuario = formulario.save()
                # El formulario ya crea el perfil médico
                messages.success(request, '¡Registro exitoso! Bienvenido a SportRoutineAI.')
                login(request, usuario)
                return redirect('dashboard')
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
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f'¡Bienvenido de nuevo, {usuario.username}!')
                next_url = request.GET.get('next', 'dashboard')
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
    return redirect('index')


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
    
    try:
        resultado = motor_recomendacion.generar_recomendacion_completa(usuario)
        
        if 'error' in resultado:
            messages.error(request, resultado['error'])
            return redirect('dashboard')
        
        # Marcar recomendaciones anteriores como no vigentes
        usuario.recomendaciones.filter(vigente=True).update(vigente=False)
        
        # Marcar la nueva como vigente
        resultado['recomendacion'].vigente = True
        resultado['recomendacion'].save()
        
        messages.success(request, '¡Nueva recomendación generada exitosamente!')
        return redirect('dashboard')
        
    except Exception as e:
        messages.error(request, f'Error al generar recomendación: {str(e)}')
        return redirect('dashboard')


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
        formulario_medico = FormularioPerfilMedico(request.POST, instance=perfil_medico)
        
        if formulario_usuario.is_valid() and formulario_medico.is_valid():
            formulario_usuario.save()
            formulario_medico.save()
            
            # Actualizar perfil médico con nuevos datos
            motor_recomendacion._actualizar_perfil_medico(usuario, perfil_medico)
            
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        formulario_usuario = FormularioActualizarUsuario(instance=usuario)
        formulario_medico = FormularioPerfilMedico(instance=perfil_medico)
    
    context = {
        'usuario': usuario,
        'perfil_medico': perfil_medico,
        'formulario_usuario': formulario_usuario,
        'formulario_medico': formulario_medico,
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
            return redirect('dashboard')
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
