#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar dependencias usando python3.11 (Soluciona el error de Pillow)
python3.11 -m pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python3.11 manage.py collectstatic --no-input

# 3. Aplicar migraciones
python3.11 manage.py migrate