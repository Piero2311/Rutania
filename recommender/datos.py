RUTINAS = [
    {
        'id': 1,
        'nombre': 'Cardio Suave',
        'descripcion': 'Rutina de bajo impacto ideal para principiantes o personas mayores. Enfocada en mejorar la salud cardiovascular sin estrés excesivo en las articulaciones.',
        'nivel': 'principiante',
        'objetivo': 'mantenimiento',
        'dias_semana': 3,
        'duracion_minutos': 30,
        'intensidad': 'baja',
        'ejercicios': [
            'Caminata rápida (15 min)',
            'Bicicleta estática (10 min)',
            'Estiramientos (5 min)'
        ],
        'plan_semanal': {
            'Lunes': 'Caminata 30 min',
            'Miércoles': 'Bicicleta estática 30 min',
            'Viernes': 'Caminata + estiramientos 30 min'
        }
    },
    {
        'id': 2,
        'nombre': 'Pérdida de Peso Intensiva',
        'descripcion': 'Programa de alta intensidad combinando cardio y entrenamiento de fuerza para maximizar la quema de calorías y acelerar la pérdida de peso.',
        'nivel': 'intermedio',
        'objetivo': 'peso',
        'dias_semana': 5,
        'duracion_minutos': 45,
        'intensidad': 'alta',
        'ejercicios': [
            'HIIT (20 min)',
            'Burpees (5 min)',
            'Saltos de cuerda (10 min)',
            'Plancha (5 min)',
            'Estiramientos (5 min)'
        ],
        'plan_semanal': {
            'Lunes': 'HIIT + Burpees',
            'Martes': 'Saltos de cuerda + Plancha',
            'Miércoles': 'HIIT completo',
            'Jueves': 'Descanso activo (caminata)',
            'Viernes': 'HIIT + Saltos',
            'Sábado': 'Circuito completo',
            'Domingo': 'Descanso'
        }
    },
    {
        'id': 3,
        'nombre': 'Musculación Avanzada',
        'descripcion': 'Rutina de entrenamiento de resistencia diseñada para desarrollo muscular avanzado con división de grupos musculares.',
        'nivel': 'avanzado',
        'objetivo': 'musculacion',
        'dias_semana': 5,
        'duracion_minutos': 60,
        'intensidad': 'alta',
        'ejercicios': [
            'Press de banca (4 series x 8-10 reps)',
            'Sentadillas (4 series x 8-10 reps)',
            'Peso muerto (4 series x 6-8 reps)',
            'Dominadas (4 series x max reps)',
            'Press militar (3 series x 10 reps)'
        ],
        'plan_semanal': {
            'Lunes': 'Pecho y tríceps',
            'Martes': 'Espalda y bíceps',
            'Miércoles': 'Piernas',
            'Jueves': 'Descanso',
            'Viernes': 'Hombros y abdomen',
            'Sábado': 'Brazos completo',
            'Domingo': 'Descanso'
        }
    },
    {
        'id': 4,
        'nombre': 'Tonificación Femenina',
        'descripcion': 'Programa de tonificación muscular con enfoque en glúteos, piernas y core. Combina pesas ligeras con ejercicios funcionales.',
        'nivel': 'intermedio',
        'objetivo': 'musculacion',
        'dias_semana': 4,
        'duracion_minutos': 40,
        'intensidad': 'media',
        'ejercicios': [
            'Sentadillas sumo (3 series x 15 reps)',
            'Peso muerto rumano (3 series x 12 reps)',
            'Hip thrust (3 series x 15 reps)',
            'Plancha lateral (3 series x 30 seg)',
            'Curl de bíceps (3 series x 12 reps)'
        ],
        'plan_semanal': {
            'Lunes': 'Glúteos y piernas',
            'Martes': 'Core y brazos',
            'Jueves': 'Piernas completo',
            'Sábado': 'Cuerpo completo'
        }
    },
    {
        'id': 5,
        'nombre': 'Cardio Moderado',
        'descripcion': 'Entrenamiento cardiovascular de intensidad moderada perfecto para mejorar la resistencia y quemar calorías de forma sostenible.',
        'nivel': 'intermedio',
        'objetivo': 'peso',
        'dias_semana': 4,
        'duracion_minutos': 40,
        'intensidad': 'media',
        'ejercicios': [
            'Correr (20 min)',
            'Ciclismo (15 min)',
            'Remo (5 min)',
            'Estiramientos dinámicos (5 min)'
        ],
        'plan_semanal': {
            'Lunes': 'Correr 40 min',
            'Miércoles': 'Ciclismo 40 min',
            'Viernes': 'Correr + Remo',
            'Domingo': 'Ciclismo suave'
        }
    },
    {
        'id': 6,
        'nombre': 'Fitness General',
        'descripcion': 'Programa equilibrado que combina cardio, fuerza y flexibilidad para mantener una buena condición física general.',
        'nivel': 'principiante',
        'objetivo': 'mantenimiento',
        'dias_semana': 3,
        'duracion_minutos': 35,
        'intensidad': 'baja',
        'ejercicios': [
            'Caminata (15 min)',
            'Ejercicios con peso corporal (15 min)',
            'Yoga o estiramientos (10 min)'
        ],
        'plan_semanal': {
            'Lunes': 'Cardio + Flexibilidad',
            'Miércoles': 'Fuerza corporal',
            'Viernes': 'Combinación completa'
        }
    },
    {
        'id': 7,
        'nombre': 'Entrenamiento Funcional',
        'descripcion': 'Rutina de movimientos funcionales que mejoran la fuerza, equilibrio y coordinación para actividades diarias.',
        'nivel': 'intermedio',
        'objetivo': 'mantenimiento',
        'dias_semana': 4,
        'duracion_minutos': 45,
        'intensidad': 'media',
        'ejercicios': [
            'Kettlebell swings (3 series x 15 reps)',
            'Box jumps (3 series x 10 reps)',
            'Turkish get-ups (2 series x 5 reps)',
            'Farmer walks (3 series x 30 seg)',
            'Battle ropes (3 series x 30 seg)'
        ],
        'plan_semanal': {
            'Lunes': 'Fuerza funcional',
            'Martes': 'Cardio funcional',
            'Jueves': 'Potencia y explosividad',
            'Sábado': 'Circuito completo'
        }
    },
    {
        'id': 8,
        'nombre': 'CrossFit para Principiantes',
        'descripcion': 'Introducción al entrenamiento de alta intensidad con movimientos funcionales variados. Versión adaptada para principiantes.',
        'nivel': 'principiante',
        'objetivo': 'musculacion',
        'dias_semana': 3,
        'duracion_minutos': 30,
        'intensidad': 'media',
        'ejercicios': [
            'Air squats (3 series x 15 reps)',
            'Push-ups modificados (3 series x 10 reps)',
            'Sit-ups (3 series x 15 reps)',
            'Jumping jacks (3 series x 20 reps)',
            'Mountain climbers (3 series x 10 reps)'
        ],
        'plan_semanal': {
            'Lunes': 'WOD básico A',
            'Miércoles': 'WOD básico B',
            'Viernes': 'WOD básico C'
        }
    },
    {
        'id': 9,
        'nombre': 'Yoga y Movilidad',
        'descripcion': 'Programa centrado en flexibilidad, movilidad articular y fortalecimiento del core mediante posturas de yoga.',
        'nivel': 'principiante',
        'objetivo': 'mantenimiento',
        'dias_semana': 3,
        'duracion_minutos': 40,
        'intensidad': 'baja',
        'ejercicios': [
            'Saludo al sol (5 repeticiones)',
            'Posturas de equilibrio (10 min)',
            'Estiramientos profundos (15 min)',
            'Respiración y meditación (10 min)'
        ],
        'plan_semanal': {
            'Lunes': 'Yoga matutino',
            'Miércoles': 'Movilidad y equilibrio',
            'Viernes': 'Yoga restaurativo'
        }
    },
    {
        'id': 10,
        'nombre': 'Definición Muscular',
        'descripcion': 'Programa avanzado que combina entrenamiento de resistencia con cardio para reducir grasa corporal manteniendo masa muscular.',
        'nivel': 'avanzado',
        'objetivo': 'peso',
        'dias_semana': 6,
        'duracion_minutos': 50,
        'intensidad': 'alta',
        'ejercicios': [
            'Superseries de pesas (25 min)',
            'Cardio HIIT (15 min)',
            'Core intensivo (10 min)',
            'Estiramientos (5 min)'
        ],
        'plan_semanal': {
            'Lunes': 'Pecho + HIIT',
            'Martes': 'Espalda + HIIT',
            'Miércoles': 'Piernas + Core',
            'Jueves': 'Hombros + HIIT',
            'Viernes': 'Brazos + Core',
            'Sábado': 'Full body + Cardio',
            'Domingo': 'Descanso activo'
        }
    }
]
