# 🔐 SECURE HTTPS DEPLOYMENT GUIDE

**School Management System with SSL/TLS**

---

## 📋 Table of Contents

1. [Docker Deployment (Recommended)](#docker-deployment)
2. [Traditional Server Deployment](#traditional-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Verification & Testing](#verification)
6. [Troubleshooting](#troubleshooting)

---

## 🐳 Docker Deployment (Recommended)

### Prerequisites

```bash
# Install Docker & Docker Compose
# macOS/Windows: Install Docker Desktop
# Linux:
sudo apt-get install docker.io docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 1: Create SSL Certificates

**Option A: Let's Encrypt (Production)**

```bash
# Install Certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your-email@example.com

# Copy to project (requires sudo)
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./certs/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./certs/key.pem
sudo chown $USER:$USER ./certs/*
```

**Option B: Self-Signed (Development)**

```bash
# Create certs directory
mkdir -p certs

# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes \
  -out certs/cert.pem \
  -keyout certs/key.pem \
  -days 365 \
  -subj "/CN=localhost"
```

### Step 2: Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env
```

**Minimum .env settings**:
```bash
# Django
SECRET_KEY=your-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_PASSWORD=your-secure-db-password

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# HTTPS (should be True for production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 3: Build & Run Docker Containers

```bash
# Build Docker image
docker-compose build

# Start all services (Django, PostgreSQL, Redis, Nginx)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web

# Check if services are healthy
docker-compose ps
# Look for "healthy" status
```

### Step 4: Access Application

```
HTTPS: https://yourdomain.com/
HTTP redirects to HTTPS automatically
```

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f web          # Django logs
docker-compose logs -f nginx        # Nginx logs
docker-compose logs -f db           # Database logs

# Execute commands in container
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py migrate

# Stop services
docker-compose down

# Rebuild after changes
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check database
docker-compose exec db psql -U postgres -d school_management

# Backup database
docker-compose exec db pg_dump -U postgres school_management > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres school_management < backup.sql
```

---

## 🖥️ Traditional Server Deployment

### Prerequisites

- Ubuntu 20.04+ or similar Linux
- Root or sudo access
- Domain name with DNS configured

### Step 1: Install Dependencies

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python, PostgreSQL, Redis, Nginx
sudo apt-get install -y \
  python3.11 \
  python3.11-venv \
  python3.11-dev \
  postgresql \
  postgresql-contrib \
  redis-server \
  nginx \
  certbot \
  python3-certbot-nginx

# Install Gunicorn
pip install gunicorn
```

### Step 2: Setup PostgreSQL

```bash
# Create database user
sudo -u postgres createuser school_user -P
# Enter password when prompted

# Create database
sudo -u postgres createdb -O school_user school_management

# Test connection
psql -h localhost -U school_user -d school_management
```

### Step 3: Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/school-management
cd /var/www/school-management

# Clone/download project files
# (or copy from your repository)

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary whitenoise

# Create .env file
cp .env.example .env
# Edit .env with your settings
nano .env

# Run migrations
python manage.py migrate --settings=config.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=config.settings_production

# Create superuser
python manage.py createsuperuser --settings=config.settings_production
```

### Step 4: Setup SSL Certificate (Let's Encrypt)

```bash
# Generate certificate
sudo certbot certonly --nginx \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your-email@example.com

# Certificates will be in:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Step 5: Configure Nginx

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/school-management
```

**Copy the content from `nginx.conf`** (update server_name and certificate paths)

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/school-management /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 6: Create Gunicorn Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/school-management.service
```

**Content**:
```ini
[Unit]
Description=School Management System
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/school-management
Environment="PATH=/var/www/school-management/venv/bin"
ExecStart=/var/www/school-management/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 30 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    config.wsgi:application

Restart=on-failure
RestartSec=10s

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

### Step 7: Setup SSL Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Enable auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Check status
sudo systemctl status certbot.timer
```

---

## 🚀 Heroku Deployment

### Step 1: Setup Heroku

```bash
# Install Heroku CLI
# macOS: brew install heroku
# Other: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create school-management

# Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0

# Add Redis
heroku addons:create heroku-redis:premium-0
```

### Step 2: Configure Environment Variables

```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secure-key
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=config.settings_production
heroku config:set ALLOWED_HOSTS=school-management.herokuapp.com,yourdomain.com

# Disable auto HTTPS redirect (Heroku handles it)
heroku config:set SECURE_SSL_REDIRECT=False

# Heroku provides DATABASE_URL automatically
```

### Step 3: Create Procfile

```bash
# Create file named "Procfile"
echo "web: gunicorn config.wsgi --log-file -" > Procfile
echo "release: python manage.py migrate --settings=config.settings_production" >> Procfile
echo "release: python manage.py collectstatic --noinput --settings=config.settings_production" >> Procfile
```

### Step 4: Create runtime.txt

```bash
echo "python-3.11.0" > runtime.txt
```

### Step 5: Deploy

```bash
# Add to git
git add .
git commit -m "Configure for Heroku deployment"

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail

# Create superuser
heroku run python manage.py createsuperuser --settings=config.settings_production
```

### Step 6: Setup Custom Domain

```bash
# Add domain
heroku domains:add yourdomain.com

# Configure DNS (see Heroku output)
# Then wait 24-48 hours for DNS propagation

# Enable automatic HTTPS
heroku certs:auto:enable
```

---

## ☁️ Cloud Platforms

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Create .ebextensions/django.config
mkdir -p .ebextensions
nano .ebextensions/django.config
```

**Content**:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: config.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: config.settings_production
  aws:elbv2:listener:default:
    Protocol: HTTP
  aws:elbv2:listener:443:
    Protocol: HTTPS
    SSLCertificateArns: arn:aws:acm:region:account-id:certificate/id
```

```bash
# Initialize and deploy
eb init -p python-3.11 school-management
eb create school-management-prod
eb deploy
```

### Google Cloud Run

```bash
# Create app.yaml
cat > app.yaml << EOF
runtime: python311
entrypoint: gunicorn -b :$PORT config.wsgi:application

env:
  DJANGO_SETTINGS_MODULE: config.settings_production
  
automatic_scaling:
  min_instances: 1
  max_instances: 10
EOF

# Deploy
gcloud app deploy
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Create `app.yaml`:

```yaml
name: school-management
services:
- name: web
  github:
    repo: your-username/school-management
    branch: main
  build_command: pip install -r requirements.txt && python manage.py collectstatic --noinput --settings=config.settings_production
  run_command: gunicorn config.wsgi:application --bind 0.0.0.0:8080
  http_port: 8080
  envs:
  - key: DJANGO_SETTINGS_MODULE
    value: config.settings_production
  - key: SECRET_KEY
    value: ${SECRET_KEY}
  - key: DEBUG
    value: "False"

databases:
- name: db
  engine: PG
  version: "15"
```

---

## 🔍 Verification & Testing

### Verify HTTPS is Working

```bash
# Check SSL certificate
openssl s_client -connect yourdomain.com:443 < /dev/null

# Check security headers
curl -I https://yourdomain.com/

# Online tools
# https://www.ssllabs.com/ssltest/
# https://securityheaders.com/
```

### Expected Security Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; ...
Referrer-Policy: strict-origin-when-cross-origin
```

### Test Login Flow

1. Navigate to `https://yourdomain.com/`
2. Verify HTTPS with padlock icon
3. Login with default credentials
4. Test student/teacher/admin functions
5. Check no mixed content warnings

### Monitor SSL Certificate

```bash
# Check expiration
openssl x509 -noout -dates -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem

# Set renewal reminder
# Let's Encrypt auto-renews 30 days before expiration
```

---

## 🐛 Troubleshooting

### "SSL certificate problem" Error

```bash
# Check certificate validity
openssl x509 -noout -dates -in /path/to/cert.pem

# Renew Let's Encrypt certificate
sudo certbot renew --force-renewal

# In Docker
docker-compose exec nginx certbot renew
```

### "Mixed Content" Warning

**Cause**: Page loaded over HTTPS but resources over HTTP

**Solution**:
```python
# In settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### "Nginx 502 Bad Gateway"

```bash
# Check if Django is running
curl http://127.0.0.1:8000/

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart Gunicorn
sudo systemctl restart school-management
```

### "Certificate refused by peer" in Docker

```bash
# Regenerate self-signed certificate
rm -rf certs
mkdir certs
openssl req -x509 -newkey rsa:4096 -nodes \
  -out certs/cert.pem \
  -keyout certs/key.pem \
  -days 365 \
  -subj "/CN=localhost"

# Restart containers
docker-compose down
docker-compose up -d
```

### "Connection refused" Error

```bash
# Check if services are running
docker-compose ps
docker-compose logs

# Verify ports are open
netstat -tulpn | grep LISTEN

# Check firewall
sudo ufw status
sudo ufw allow 80,443/tcp
```

---

## 📊 Performance Monitoring

### Monitor SSL Handshake

```bash
# Time SSL connection
curl -w "time_connect: %{time_connect}\ntime_appconnect: %{time_appconnect}\n" \
  -o /dev/null -s https://yourdomain.com/
```

### Check Certificate Chain

```bash
# Verify full chain
openssl s_client -connect yourdomain.com:443 -showcerts
```

### Monitor Certificate Expiration

```bash
# Check days until expiration
certbot certificates

# Set alert (example: 30 days)
certbot renew --dry-run
```

---

## ✅ Production Checklist

```
HTTPS/SSL
- [ ] SSL certificate installed
- [ ] Certificate auto-renewal enabled
- [ ] Certificate valid for all domains
- [ ] No certificate warnings in browser

Django Configuration
- [ ] DEBUG = False
- [ ] SECRET_KEY is secure
- [ ] ALLOWED_HOSTS configured
- [ ] SECURE_SSL_REDIRECT = True
- [ ] Cookies marked as Secure

Security Headers
- [ ] HSTS enabled
- [ ] X-Frame-Options set
- [ ] X-Content-Type-Options set
- [ ] CSP configured
- [ ] No mixed content warnings

Database
- [ ] PostgreSQL in production
- [ ] Database backups configured
- [ ] Connection encrypted
- [ ] User credentials secure

Monitoring
- [ ] Error logging enabled
- [ ] Access logs enabled
- [ ] SSL expiration alerts set
- [ ] Uptime monitoring enabled

Performance
- [ ] Static files served efficiently
- [ ] Compression enabled
- [ ] Caching configured
- [ ] Database optimized

Testing
- [ ] Login/logout works
- [ ] All forms submit over HTTPS
- [ ] No SSL warnings
- [ ] Security headers verified
```

---

## 📚 Additional Resources

- [Django Deployment Documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx SSL Configuration](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)

---

**Your School Management System is now Secure with HTTPS! 🔒✅**
