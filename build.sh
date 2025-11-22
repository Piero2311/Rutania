#!/usr/bin/env bash
set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Build completado exitosamente!"

