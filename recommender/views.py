from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .datos import RUTINAS
from . import processor
from . import logic_rules


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
