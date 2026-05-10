# Production Settings for HTTPS/SSL

This file explains how to configure the School Management System for secure HTTPS deployment.

## 🔐 Environment Variables for HTTPS

Create a `.env` file in your project root with these settings:

```bash
# Django Settings
SECRET_KEY=your-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# HTTPS Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/school_management

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Trusted Origins (if behind reverse proxy)
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔒 SSL/TLS Certificate Options

### Option 1: Let's Encrypt (FREE & RECOMMENDED)

**Install Certbot**:
```bash
# Ubuntu/Debian
sudo apt-get install certbot python3-certbot-nginx

# macOS (Homebrew)
brew install certbot
```

**Generate Certificate**:
```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

Certificates stored at:
- `/etc/letsencrypt/live/yourdomain.com/fullchain.pem` (Certificate)
- `/etc/letsencrypt/live/yourdomain.com/privkey.pem` (Private Key)

**Auto-Renewal**:
```bash
sudo certbot renew --dry-run  # Test renewal
sudo systemctl enable certbot.timer  # Auto-renew
```

### Option 2: Self-Signed Certificate (DEV/TESTING ONLY)

```bash
# Generate self-signed certificate (valid 365 days)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Follow prompts to fill in certificate details
```

### Option 3: Commercial SSL Certificate

- Buy from: Comodo, DigiCert, GoDaddy, AWS Certificate Manager
- Follow provider's instructions for installation
- Typically: certificate.crt + private.key files

## 🚀 Nginx Configuration for HTTPS

Create `/etc/nginx/sites-available/school-management`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration (Security Best Practices)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data: https:; font-src 'self' cdn.jsdelivr.net;" always;
    
    # Gzip Compression
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;
    gzip_min_length 1000;
    
    # Proxy Settings
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static Files
    location /static/ {
        alias /var/www/school-management/staticfiles/;
        expires 30d;
    }
    
    # Media Files
    location /media/ {
        alias /var/www/school-management/media/;
        expires 30d;
    }
}

# Redirect www to non-www (optional)
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    return 301 https://yourdomain.com$request_uri;
}
```

Enable Nginx site:
```bash
sudo ln -s /etc/nginx/sites-available/school-management /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## 🐍 Gunicorn Configuration with HTTPS

Create `gunicorn.conf.py`:

```python
import multiprocessing

# Binding
bind = "127.0.0.1:8000"

# Workers (CPU cores * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
graceful_timeout = 30

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process Naming
proc_name = "school-management"

# Server Mechanics
daemon = False
umask = 0
pidfile = "/var/run/gunicorn.pid"
```

Run Gunicorn:
```bash
gunicorn config.wsgi:application --config gunicorn.conf.py
```

## 🔧 Systemd Service for Auto-Start

Create `/etc/systemd/system/school-management.service`:

```ini
[Unit]
Description=School Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/school-management
ExecStart=/var/www/school-management/venv/bin/gunicorn config.wsgi:application --config gunicorn.conf.py

# Auto-restart on failure
Restart=on-failure
RestartSec=10s

# Environment variables
EnvironmentFile=/var/www/school-management/.env

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable school-management
sudo systemctl start school-management
sudo systemctl status school-management
```

## 🔐 Django HTTPS Configuration

Update `config/settings.py`:

```python
import os

# Force HTTPS
SECURE_SSL_REDIRECT = True

# Cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
X_CONTENT_TYPE_OPTIONS = 'nosniff'

# Allowed hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

## 📋 Pre-Deployment Checklist

```
HTTPS/SSL Setup
- [ ] Generated SSL certificate (Let's Encrypt or commercial)
- [ ] Configured Nginx with SSL settings
- [ ] Set up certificate auto-renewal
- [ ] Tested HTTPS connection

Django Configuration
- [ ] Changed SECRET_KEY to secure random value
- [ ] Set DEBUG = False
- [ ] Updated ALLOWED_HOSTS
- [ ] Configured SECURE_SSL_REDIRECT = True
- [ ] Enabled SESSION_COOKIE_SECURE = True
- [ ] Enabled CSRF_COOKIE_SECURE = True

Database
- [ ] Switched to PostgreSQL (from SQLite)
- [ ] Set up database backups
- [ ] Tested database connection with credentials

Static Files
- [ ] Collected static files: python manage.py collectstatic
- [ ] Configured Nginx to serve static files
- [ ] Verified CSS/JS loading

Security Headers
- [ ] Added HSTS headers
- [ ] Added X-Frame-Options
- [ ] Added X-Content-Type-Options
- [ ] Added CSP (Content Security Policy)

Monitoring
- [ ] Set up SSL certificate monitoring/alerts
- [ ] Configured error logging
- [ ] Set up uptime monitoring

Testing
- [ ] Tested HTTPS connection
- [ ] Verified certificate chain
- [ ] Checked security headers (https://securityheaders.com)
- [ ] Tested login/logout flow
- [ ] Tested form submissions
```

## 🧪 Testing HTTPS Locally (Development)

### Generate Self-Signed Certificate:

```bash
# Create certificates directory
mkdir -p certs

# Generate private key
openssl genrsa -out certs/key.pem 2048

# Generate certificate
openssl req -new -x509 -key certs/key.pem -out certs/cert.pem -days 365

# When prompted:
# Country Name: US
# State: California
# Locality: San Francisco
# Organization: Your School
# Organization Unit: IT
# Common Name: localhost
```

### Run Django with HTTPS (using runserver_plus):

```bash
pip install django-extensions werkzeug
python manage.py runserver_plus --cert-file=certs/cert.pem --key-file=certs/key.pem
```

Access at: `https://localhost:8000/`

(Accept self-signed certificate warning in browser)

## 🔍 Verify SSL/TLS Configuration

**Check certificate details**:
```bash
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem -text -noout
```

**Test SSL/TLS strength**:
```bash
# Using nmap
nmap --script ssl-enum-ciphers -p 443 yourdomain.com

# Using testssl.sh
bash testssl.sh https://yourdomain.com
```

**Check security headers**:
```bash
curl -I https://yourdomain.com
# Look for: Strict-Transport-Security, X-Frame-Options, etc.
```

## 🌐 Production Deployment Platforms (HTTPS Built-in)

These platforms handle HTTPS/SSL automatically:

1. **Heroku** (Recommended for beginners)
   - Free SSL certificate included
   - Custom domain setup
   ```bash
   git push heroku main
   ```

2. **PythonAnywhere**
   - One-click HTTPS setup
   - Free certificate from Let's Encrypt

3. **AWS (Elastic Beanstalk)**
   - Integration with AWS Certificate Manager
   - Auto-renewal

4. **Google Cloud Platform**
   - Google-managed certificates
   - Cloud Load Balancer with SSL

5. **DigitalOcean App Platform**
   - Automatic HTTPS
   - Free Let's Encrypt certificates

## 📚 Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/4.2/topics/security/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx SSL Best Practices](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)

## ✅ Security Checklist Summary

```
✓ HTTPS/SSL Certificate installed
✓ Nginx configured with secure SSL settings
✓ Django SECURE_SSL_REDIRECT enabled
✓ Cookies configured as Secure & HttpOnly
✓ HSTS headers enabled
✓ CSP (Content Security Policy) configured
✓ Security headers set (X-Frame-Options, X-Content-Type-Options)
✓ CSRF protection enabled
✓ DEBUG set to False
✓ SECRET_KEY randomized
✓ Database secured
✓ Static files collected
✓ Logging configured
✓ Monitoring enabled
```

---

**Your School Management System is now Secure with HTTPS! 🔒**
