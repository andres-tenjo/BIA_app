from pathlib import Path
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't2eewzw__782f5#si&tf*y4_6p(_l@njd^5zltfbzu^=mkrw@d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['env-biapp.eba-avt2aqwt.us-west-2.elasticbeanstalk.com']
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'rest_framework',
    'bootstrap4',
    'import_export',
    'widget_tweaks',
    # Apps
    'apps.home',
    'apps.modulo_comercial',
    'apps.modulo_compras',
    'apps.modulo_logistica',
    'apps.modulo_indicadores',
    'apps.modulo_reportes',
    'apps.modulo_configuracion',
    'apps.planeacion',
    'apps.usuario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'biapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join((BASE_DIR), 'templates/')],
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

WSGI_APPLICATION = 'biapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'appbia',
#         'USER': 'postgres',
#         'PASSWORD': '    ',
#         'HOST': '127.0.0.1',
#         'DATABSE_PORT': '5432',
#     }
# }



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = 'static'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]

LOGIN_REDIRECT_URL = reverse_lazy('home')

LOGOUT_REDIRECT_URL = reverse_lazy('login')

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'usuario.User'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

IMPORT_EXPORT_USE_TRANSACTIONS = True

<<<<<<< HEAD
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800000
=======
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000
>>>>>>> 9c9067de1080b614bf4582bd8bbad78196954851
