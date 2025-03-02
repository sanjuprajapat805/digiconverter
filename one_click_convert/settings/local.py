from os import getenv, path
from datetime import timedelta
from dotenv import load_dotenv
from .base import * #noqa
from .base import BASE_DIR


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv("ADMIN_URL")

DOMAIN = getenv("DOMAIN")

CSRF_COOKIE_SECURE = False  # Only for development
SESSION_COOKIE_SECURE = False  # Only for development

LOCKOUT_DURATION = timedelta(minutes=1)

LOGIN_ATTEMPTS = 3