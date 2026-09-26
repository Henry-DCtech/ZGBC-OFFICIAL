import os
from pathlib import Path
from dotenv import load_dotenv



load_dotenv()  # Load .env file for environment variables

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/'        # This wins
LOGIN_REDIRECT_URL = 'core:home'     # This wins, the 'core:home' above it is ignored
LOGOUT_REDIRECT_URL = '/'   # This wins

# DEBUG = os.getenv('DEBUG', 'False') == 'True'


SECRET_KEY = 'change-this-in- domain production'


ALLOWED_HOSTS = ['*']
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-domain.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'crispy_forms',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #.... Other App
    'core',
    #rd party = install with: pip...
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = 'core.CustomUser'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or smtp.gmail.com if using Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'zionglobalbiblechurch@gmail.com'  # your full email
EMAIL_HOST_PASSWORD = 'tech@1234'
DEFAULT_FROM_EMAIL = 'Zion Global Bible Church <zionglobalbiblechurch@gmail.com>'
SERVER_EMAIL = 'zionglobalbiblechurch@gmail.com'
ADMIN_EMAIL: 'henrytech727@gmail.com' # type: ignore
SITE_URL = 'https://127.0.0.1:8000'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'htmlmin.middleware.HtmlMinifyMiddleware',
    # 'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #....other Middleware
    'core.middleware.LoginRequiredMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'core.middleware.OnlineUsersMiddleware',
]

ROOT_URLCONF = 'church_media.urls'

TEMPLATES = [{
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
}]

WSGI_APPLICATION = 'church_media.wsgi.application'

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'church_db',
        'USER': 'postgres',
        'PASSWORD': 'idoreyin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Static files for production
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_WEBHOOK_SECRET = os.getenv('PAYSTACK_WEBHOOK_SECRET')

#EMAIL ADMIN
DEFAULT_FROM_EMAIL = 'ZGBC OFFICIAL<no-reply@zionglobalbiblechurch@gmail.com>'
ADMIN_EMAIL = 'admin@zionglobalbiblechurch@gmail.com'  # Gets copy of all donations
