"""
Django settings for ulearn_vacs_project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v$ghmvh%_ms2ei5te@t)x#3$%ov3%5h%t(8ar-l%5@5haosxe4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ["ve3xone.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'general_page',
    'general_stats_page',
    'relevance_page',
    'geography_page',
    'skills_page',
    'latest_vacs_page',
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

ROOT_URLCONF = 'ulearn_vacs_project.urls'

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

WSGI_APPLICATION = 'ulearn_vacs_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = '/home/ve3xone/django/static' # For pythonanywhere (python manage.py collectstatic)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_VAC_TEXT = r"""<p class="">
    Добро пожаловать на главную страницу профессии Java-программиста! Java-программирование — это одна из самых популярных и универсальных областей разработки, которая используется для создания надежных, масштабируемых и производительных приложений как на стороне сервера, так и на стороне клиента.
</p>

<p class="">
    Ваша роль в качестве Java-программиста включает разработку приложений, которые могут охватывать самые разные сферы: от веб-сервисов и корпоративных систем до мобильных приложений для Android и сложных распределённых систем. Используя мощь языка Java, вы создаёте решения, которые обеспечивают стабильную работу в различных средах и операционных системах.
</p>

<p class="">
    Java-программисты активно применяют такие фреймворки, как Spring, Hibernate, и JavaFX, а также работают с технологиями для управления базами данных, включая JDBC и JPA. Ваша работа может включать создание RESTful API, интеграцию с внешними системами и оптимизацию производительности приложений для обработки большого объема данных.
</p>

<p class="">
    Одной из основных задач Java-разработчика является проектирование архитектуры приложений, обеспечивающей их безопасность, масштабируемость и высокую производительность. Ваше глубокое понимание объектно-ориентированного программирования, структур данных и алгоритмов делает вас мастером своего дела.
</p>

<p class="">
    Кроме того, Java-программисты тесно взаимодействуют с другими членами команды: аналитиками, тестировщиками, дизайнерами и менеджерами проектов. Совместная работа позволяет разрабатывать решения, которые отвечают всем требованиям заказчика и превосходят ожидания пользователей.
</p>

<p class="">
    Для успешной карьеры Java-программиста важны не только технические навыки, но и способность к анализу, коммуникации и решению сложных задач. Постоянное изучение новых библиотек, технологий и подходов помогает вам оставаться конкурентоспособным в быстро развивающемся мире IT.
</p>

<p class="">
    Работа Java-программиста — это не просто написание кода, а решение реальных задач бизнеса и общества с помощью современных технологий. Вы создаёте надёжные и эффективные приложения, которые помогают автоматизировать процессы, улучшать пользовательский опыт и открывать новые возможности для компаний и людей по всему миру.
</p>"""
