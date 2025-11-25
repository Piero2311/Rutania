#!/usr/bin/env bash
set -o errexit

echo "Actualizando pip..."
pip install --upgrade pip

echo "Instalando dependencias Python..."
pip install -r requirements.txt

echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Cargando rutinas en la base de datos..."
python manage.py cargar_rutinas --verbosity=0 || echo "⚠️  Advertencia: No se pudieron cargar rutinas (puede que ya existan)"

echo "✅ Build completado"
