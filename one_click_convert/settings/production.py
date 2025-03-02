from os import getenv, path
from datetime import timedelta
from .base import * #noqa
from .base import BASE_DIR
import dj_database_url

# Load production environment variables from file
prod_env_file = path.join(BASE_DIR, ".env.production")

if path.isfile(prod_env_file):
    from dotenv import load_dotenv
    load_dotenv(prod_env_file)

# Core settings
SECRET_KEY = getenv("SECRET_KEY")
DEBUG = getenv("DEBUG", "False").lower() in ("true", "1", "yes")
SITE_NAME = getenv("SITE_NAME")
DOMAIN = getenv("DOMAIN", "")
ALLOWED_HOSTS = [DOMAIN, f"www.{DOMAIN}"] if DOMAIN else []
ADMIN_URL = getenv("ADMIN_URL")

# CSRF settings
#allow front end url or load balancer urls
CSRF_TRUSTED_ORIGINS = getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if getenv("CSRF_TRUSTED_ORIGINS") else []

# Authentication & Security Settings
LOCKOUT_DURATION = timedelta(minutes=10)
LOGIN_ATTEMPTS = 3
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = getenv("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "yes")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(getenv("SECURE_HSTS_SECONDS", 300))
SECURE_HSTS_INCLUDE_SUBDOMAINS = getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() in ("true", "1", "yes")
SECURE_HSTS_PRELOAD = getenv("SECURE_HSTS_PRELOAD", "True").lower() in ("true", "1", "yes")
SECURE_CONTENT_TYPE_NOSNIFF = getenv("SECURE_CONTENT_TYPE_NOSNIFF", "True").lower() in ("true", "1", "yes")

SECURE_CONTENT_TYPE_NOSNIFF = getenv("SECURE_CONTENT_TYPE_NOSNIFF")

# Database configuration using dj-database-url
# DATABASE_URL = getenv("DATABASE_URL", "")
# DATABASES = {
#     "default": dj_database_url.config(default=DATABASE_URL) if DATABASE_URL else {}
# }

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware",]