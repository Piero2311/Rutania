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

echo "✅ Build completado"
