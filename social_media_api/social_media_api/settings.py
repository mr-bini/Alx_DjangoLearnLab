import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Use PostgreSQL in production
        'NAME': os.getenv('DB_NAME', 'social_media_db'),       # ✅ Database name
        'USER': os.getenv('DB_USER', 'db_user'),               # ✅ Database user
        'PASSWORD': os.getenv('DB_PASSWORD', 'securepassword'),# ✅ Database password
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),                  # ✅ Database port
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your production domain(s)
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_BROWSER_XSS_FILTER = True        # Enables browser XSS protection
X_FRAME_OPTIONS = 'DENY'                # Prevents clickjacking
SECURE_SSL_REDIRECT = True              # Redirect all HTTP to HTTPS
