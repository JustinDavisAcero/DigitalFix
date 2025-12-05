#!/usr/bin/env bash
set -o errexit

# Actualizar pip
python3.11 -m pip install --upgrade pip --break-system-packages

# Instalar dependencias
python3.11 -m pip install -r requirements.txt --break-system-packages

# Asegurar instalación de gunicorn
python3.11 -m pip install gunicorn --break-system-packages

# Recolectar estáticos
python3.11 manage.py collectstatic --noinput

# Migraciones
python3.11 manage.py migrate
