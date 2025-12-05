#!/usr/bin/env bash
set -o errexit

# Asegurar pip actualizado
python3.11 -m pip install --upgrade pip

# Instalar dependencias EN python3.11
python3.11 -m pip install -r requirements.txt

# FORZAR la instalación de gunicorn dentro de Python3.11
python3.11 -m pip install gunicorn

# Recolectar archivos estáticos
python3.11 manage.py collectstatic --no-input

# Aplicar migraciones
python3.11 manage.py migrate