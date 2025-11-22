# Procfile para Heroku y otras plataformas compatibles
# Si usas Render.com, no necesitas este archivo (usa render.yaml)

web: gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate --noinput

