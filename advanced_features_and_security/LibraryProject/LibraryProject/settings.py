# SECURITY CONFIGURATIONS

# Never keep DEBUG=True in production
DEBUG = False  

# Security middleware options
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cookies should only be sent over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Use the custom user model
AUTH_USER_MODEL = "bookshelf.CustomUser"
