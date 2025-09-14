# SECURITY CONFIGURATIONS

DEBUG = False

# Security middleware options
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cookies should only be sent over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Force HTTPS
SECURE_SSL_REDIRECT = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Use the custom user model
AUTH_USER_MODEL = "bookshelf.CustomUser"
