#!/usr/bin/env bash
set -o errexit

# Actualizar pip
python3.11 -m pip install --upgrade pip

# Instalar dependencias en python3.11
python3.11 -m pip install -r requirements.txt

# Instalar gunicorn en python3.11 (IMPORTANTE)
python3.11 -m pip install gunicorn

# Collect static
python3.11 manage.py collectstatic --noinput

# Migraciones
python3.11 manage.py migrate
