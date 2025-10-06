# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your production domain(s)
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_BROWSER_XSS_FILTER = True        # Enables browser XSS protection
X_FRAME_OPTIONS = 'DENY'                # Prevents clickjacking
SECURE_SSL_REDIRECT = True              # Redirect all HTTP to HTTPS
