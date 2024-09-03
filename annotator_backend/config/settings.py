"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# 获取当前目录
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'upload/json'),)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fb#=1ahd0&-8)w1feazrq%f#dzg9!^+at$eh0ke8@$@u(2*2s8'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000  # 根据你的需要设置一个合适的值

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 定时任务
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dataset',
    'requester',
    'worker',
    'sign',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.log_middleware.LogMiddle',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

ENV_PROFILE = os.getenv("annotator")
if ENV_PROFILE == "production":
    # 生产环境数据库
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rowing-annotator',
            'USER': 'root',
            'PASSWORD': '12345678',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
else:
    # 开发环境数据库
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rowing-annotator',
            'USER': 'root',
            'PASSWORD': '12345678',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 拓展user表
AUTH_USER_MODEL = 'sign.UserInfo'

LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    # 禁用日志
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            # 将系统接受到的体制，交给handler去处理
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, "info.logs"),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            # 'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        'console': {
            'filename': os.path.join(LOGGING_DIR, "info.logs"),
            # 'filter': ['require_debug_true'],
            'level': 'INFO',
            # 指定日志的格式
            'formatter': '',
            # 备份
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件大小：5M
            'maxBytes': 5 * 1024 * 1024,
            'encoding': "utf-8"
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(message)s'
        }
    }
}


# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
# 对应的发送的请求的跨域
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
# 未登录重定向链接

# 前端可以拿到cookie的值
SESSION_COOKIE_HTTPONLY = False

# session设置
SESSION_COOKIE_AGE = 12 * 60 * 60  # 30分钟


