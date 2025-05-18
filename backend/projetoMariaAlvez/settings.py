import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7*9%=-fxa#a@bzgi-a_l+4)^w79p&8lr$#mo3a4$l7&emq#5e2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'projetoMariaAlvezApp.apps.projetoMariaAlvezAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projetoMariaAlvez.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'projetoMariaAlvez.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'centro_de_bem_estar_maria_alvez'),
        'USER': os.getenv('DB_USER', 'admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'adminadmin'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "projetoMariaAlvezApp/static"]
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin settings for Django Admin customization
JAZZMIN_SETTINGS = {
    "site_logo": "img/logo.png",
    "site_logo_classes": "img-circle elevation-3",
    "site_title": "Centro de Bem Estar Animal - Maria Alvez",
    "site_header": "Centro de Bem Estar Animal - Maria Alvez",
    "site_brand": "CBEA Maria Alves",
    "welcome_sign": "Centro de Bem Estar Animal Maria Alvez",
    "copyright": "CBEA Maria Alves",
    "custom_css": "css/custom_admin.css",

    "topmenu_links": [
        {"name": "Início", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "projetoMariaAlvezApp.Tutor"},
        {"model": "projetoMariaAlvezApp.Animal"},
    ],

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "projetoMariaAlvezApp.Tutor": "fas fa-user",
        "projetoMariaAlvezApp.Animal": "fas fa-dog",
        "projetoMariaAlvezApp.ConsultaClinica": "fas fa-stethoscope",
        "projetoMariaAlvezApp.Cirurgia": "fas fa-cut",
        "projetoMariaAlvezApp.Vacina": "fas fa-syringe",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar": "navbar-dark bg-primary",
    "accent": "accent-info",
    "sidebar": "sidebar-dark-primary",
    "primary": "primary",

    "custom_theme": {
        "--primary": "#006699",
        "--accent": "#4CAF50",
        "--success": "#4CAF50",
        "--info": "#006699",
        "--warning": "#FFA726",
        "--danger": "#D64541",
        "--light": "#ffffff",
        "--dark": "#2f2f2f",
        "--body-bg": "#f4f6f9",
        "--text-color": "#212529",
    }
}

# Configuração para debug (para evitar problemas com arquivos estáticos)
if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'