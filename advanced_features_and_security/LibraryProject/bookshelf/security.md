# Security Configurations for LibraryProject

1. Enforced HTTPS with `SECURE_SSL_REDIRECT = True`.
2. Configured HSTS (`SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`).
3. Enforced secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`).
4. Added security headers (`X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`).
5. Configured deployment server (Nginx/Apache) to handle SSL/TLS using Let’s Encrypt certificates.
