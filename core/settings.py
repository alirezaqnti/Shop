from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
import os

# import djcelery

# djcelery.setup_loader()
# region Default Settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

# region Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jalali_date",
    "corsheaders",
    "mptt",
    "rest_framework",
    "rest_framework.authtoken",
    "ckeditor",
    "ckeditor_uploader",
    "django_cron",
    "colorfield",
    "Users",
    "Main",
    "Products",
    "Analytic",
    "Warehouse",
    "Blog",
]

# endregion


# region MiddleWare

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# endregion
try:
    from .Private import (
        DEBUG,
        DATABASES,
        CACHES,
        STATIC_ROOT,
        STATIC_URL,
        MEDIA_ROOT,
        MEDIA_URL,
        ALLOWED_HOSTS,
        REFFERER,
    )
except:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1"]
    REFFERER = "http://127.0.0.1:8000/"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # region CACHES
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379",
        }
    }

    # endregion

    # region STATIC
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    STATIC_URL = "/static/"

    # endregion

    # region MEDIA
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    # endregion


ROOT_URLCONF = "core.urls"

ASGI_APPLICATION = "core.asgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MAX_UPLOAD_SIZE = 5242880

# endregion
# region CRON

CRON_CLASSES = ["core.cronjob.QuantityCheck"]

# endregion

# region Celery
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_TIMEZONE = "Iran/Tehran"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60

# endregion


# region Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "Main.context_processors.Con",
                # "Analytic.views.VisitPage",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# endregion

# region Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# endregion

# region Internationalization

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "fa"

# locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")
TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# endregion


# region Session Setting

# SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# SESSION_CACHE_ALIAS = "default"  # or comfortabley anything else
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_AGE = 10000000
# endregion

# region Rest FrameWork

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
}

# endregion

# region debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
# endregion

# region CKEDITOR
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
}
# endregion

JALALI_DATE_DEFAULTS = {
    "Strftime": {
        "date": "%y/%m/%d",
        "datetime": "%H:%M:%S _ %y/%mm/%d",
    },
    "Static": {
        "js": [
            "admin/js/django_jalali.min.js",
        ],
        "css": {
            "all": [
                "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            ]
        },
    },
}

# region CORS

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8001",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CORS_ALLOW_CREDENTIALS = True

# endregion

# region Email Conf
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_HOST = "mail.darmaniran.com"
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "info@darmaniran.com"
# EMAIL_HOST_PASSWORD = "AbzarBehine1400"

# endregion


# region LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
# endregion


pbKEYn = 7103911361751289296658388830746844227983219246289797730958985648971967279708296739736792579263687929546606918383482400680235043342107525818413503464325971
pbKEYe = 65537
prKEYd = 2972311113578316123772367977293883082465292200627318058205690609586345341519248303895066173321944931813135020998013444255269957602943741946502311933902073
prKEYp = (
    4731199765390719506094051066379241046338305937891657841571405284305548516145942981
)
prKEYq = 1501503152269585625202396327858355883810508305252554689784338601803188791
