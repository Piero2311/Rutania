"""
Comando de management para cargar rutinas desde datos.py a la base de datos.
"""
from django.core.management.base import BaseCommand
from recommender.models import Rutina
from recommender.datos import RUTINAS


class Command(BaseCommand):
    help = 'Carga las rutinas desde datos.py a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--actualizar',
            action='store_true',
            help='Actualiza rutinas existentes en lugar de solo crear nuevas',
        )

    def handle(self, *args, **options):
        self.stdout.write('Cargando rutinas en la base de datos...')
        
        rutinas_creadas = 0
        rutinas_actualizadas = 0
        
        for rutina_data in RUTINAS:
            # Convertir duracion_minutos a formato de duracion
            duracion = f"{rutina_data.get('duracion_minutos', 30)} minutos"
            
            # Calcular calorías estimadas si no están en los datos
            calorias_estimadas = rutina_data.get('calorias_estimadas', 0)
            if calorias_estimadas == 0:
                # Estimación básica basada en duración e intensidad
                duracion_min = rutina_data.get('duracion_minutos', 30)
                intensidad = rutina_data.get('intensidad', 'media')
                peso_promedio = 70  # Peso promedio para cálculo
                if intensidad == 'alta':
                    calorias_estimadas = int((duracion_min / 60) * peso_promedio * 10)
                elif intensidad == 'media':
                    calorias_estimadas = int((duracion_min / 60) * peso_promedio * 7)
                else:
                    calorias_estimadas = int((duracion_min / 60) * peso_promedio * 5)
            
            rutina_dict = {
                'nombre': rutina_data['nombre'],
                'descripcion': rutina_data['descripcion'],
                'dias_semana': rutina_data['dias_semana'],
                'nivel': rutina_data['nivel'],
                'objetivo': rutina_data['objetivo'],
                'ejercicios': rutina_data['ejercicios'],
                'duracion': duracion,
                'intensidad': rutina_data['intensidad'],
                'calorias_estimadas': calorias_estimadas,
                'activa': True,
            }
            
            if options['actualizar']:
                rutina, created = Rutina.objects.update_or_create(
                    nombre=rutina_data['nombre'],
                    defaults=rutina_dict
                )
                if created:
                    rutinas_creadas += 1
                else:
                    rutinas_actualizadas += 1
            else:
                # Solo crear si no existe
                rutina, created = Rutina.objects.get_or_create(
                    nombre=rutina_data['nombre'],
                    defaults=rutina_dict
                )
                if created:
                    rutinas_creadas += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Rutina creada: {rutina.nombre}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⊘ Rutina ya existe: {rutina.nombre}')
                    )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Proceso completado: {rutinas_creadas} rutinas creadas, '
                f'{rutinas_actualizadas} actualizadas'
            )
        )
        
        total_rutinas = Rutina.objects.filter(activa=True).count()
        self.stdout.write(
            self.style.SUCCESS(f'Total de rutinas activas en BD: {total_rutinas}')
        )

