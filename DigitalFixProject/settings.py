import os
import dj_database_url
from pathlib import Path
import mimetypes

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a_k)7^f*5ld2#5k-*(#d2$3segz9!s#8mrb7y7(8k*8bj^2nd%'
DEBUG = 'RENDER' not in os.environ   # Render desactiva DEBUG automáticamente

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Render agrega su hostname automáticamente
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reparaciones.apps.ReparacionesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Required for serving static files on Render
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DigitalFixProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DigitalFixProject.wsgi.application'

# ---------------------------
# 🔹 Base de datos Render
# ---------------------------
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",  # Valor de respaldo si Render no da DB
        conn_max_age=600,
        ssl_require=False
    )
}

# ---------------------------
# 🔹 Validadores de contraseña
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# 🔹 Configuración regional
# ---------------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ---------------------------
# 🔹 Archivos estáticos (Render)
# ---------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'DigitalFixProject' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise para servir CSS/JS en producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# 🔹 Email temporal
# ---------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@mi-taller.com"

# ---------------------------
# 🔹 Arreglo de MIME
# ---------------------------
mimetypes.add_type("text/css", ".css", True)

# ---------------------------
# 🔹 Render CSRF
# ---------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com'
]
