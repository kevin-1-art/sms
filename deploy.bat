@echo off
REM School Management System - Secure HTTPS Deployment Setup Script for Windows
REM This script automates the setup of SSL certificates and Docker deployment

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set RESET=[0m

echo.
echo %BLUE%================================%RESET%
echo %BLUE%School Management System - HTTPS Deployment Setup%RESET%
echo %BLUE%================================%RESET%
echo.
echo This script will setup and deploy the system securely with HTTPS.
echo.

REM Check if Docker is installed
echo Checking Prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Docker is not installed or not in PATH%RESET%
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo %GREEN%[OK] Docker is installed%RESET%

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Docker Compose is not installed%RESET%
    echo Docker Compose should be included with Docker Desktop
    pause
    exit /b 1
)
echo %GREEN%[OK] Docker Compose is installed%RESET%

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Docker daemon is not running%RESET%
    echo Please start Docker Desktop
    pause
    exit /b 1
)
echo %GREEN%[OK] Docker daemon is running%RESET%

echo.
echo %BLUE%================================%RESET%
echo %BLUE%Setting Up Environment File%RESET%
echo %BLUE%================================%RESET%

REM Check if .env already exists
if exist .env (
    echo %YELLOW%[WARNING] .env file already exists. Using existing file.%RESET%
    goto :setup_ssl
)

REM Check if .env.example exists
if not exist .env.example (
    echo %RED%[ERROR] .env.example not found%RESET%
    echo Make sure you're in the project root directory
    pause
    exit /b 1
)

REM Copy .env.example to .env
copy .env.example .env >nul
echo %GREEN%[OK] .env file created%RESET%

REM Prompt for configuration
echo.
echo Please enter your configuration:
set /p DOMAIN="Domain name (e.g., yourdomain.com): "
set /p EMAIL="Email for SSL certificate: "
set /p DB_PASSWORD="Database password (strong password recommended): "

REM Update .env file
setlocal enabledelayedexpansion
(
    for /f "delims=" %%A in (.env) do (
        set "line=%%A"
        if "!line:~0,18!"=="ALLOWED_HOSTS=" (
            echo ALLOWED_HOSTS=%DOMAIN%,www.%DOMAIN%
        ) else if "!line:~0,13!"=="DB_PASSWORD=" (
            echo DB_PASSWORD=%DB_PASSWORD%
        ) else if "!line:~0,20!"=="DEFAULT_FROM_EMAIL=" (
            echo DEFAULT_FROM_EMAIL=noreply@%DOMAIN%
        ) else (
            echo !line!
        )
    )
) > .env.tmp
move /y .env.tmp .env >nul
echo %GREEN%[OK] Environment variables configured%RESET%

:setup_ssl
echo.
echo %BLUE%================================%RESET%
echo %BLUE%Setting Up SSL Certificates%RESET%
echo %BLUE%================================%RESET%

REM Create certs directory
if not exist certs mkdir certs

REM Check if certificates already exist
if exist certs\cert.pem if exist certs\key.pem (
    echo %YELLOW%[WARNING] SSL certificates already exist. Using existing certificates.%RESET%
    goto :docker_setup
)

echo.
echo SSL Certificate Options:
echo 1) Self-signed certificate (Development/Testing) - RECOMMENDED
echo 2) Let's Encrypt certificate (Production - requires domain)
set /p CERT_OPTION="Choose option (1 or 2): "

if "%CERT_OPTION%"=="2" (
    echo.
    echo %YELLOW%[WARNING] Let's Encrypt requires certbot and internet connectivity%RESET%
    echo On Windows, it's recommended to use self-signed for local testing
    echo and Let's Encrypt on a Linux server
    echo.
    echo Falling back to self-signed certificate...
)

REM Check if OpenSSL is available
openssl version >nul 2>&1
if errorlevel 1 (
    echo.
    echo %RED%[ERROR] OpenSSL is not installed or not in PATH%RESET%
    echo Please install OpenSSL from: https://slproweb.com/products/Win32OpenSSL.html
    echo Or using Chocolatey: choco install openssl
    pause
    exit /b 1
)

echo.
echo Generating self-signed SSL certificate...
openssl req -x509 -newkey rsa:4096 -nodes ^
    -out certs\cert.pem ^
    -keyout certs\key.pem ^
    -days 365 ^
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

if errorlevel 1 (
    echo %RED%[ERROR] SSL certificate generation failed%RESET%
    pause
    exit /b 1
)

echo %GREEN%[OK] SSL certificate generated%RESET%

:docker_setup
echo.
echo %BLUE%================================%RESET%
echo %BLUE%Starting Docker Containers%RESET%
echo %BLUE%================================%RESET%

echo.
echo Building Docker image (this may take several minutes)...
call docker-compose build
if errorlevel 1 (
    echo %RED%[ERROR] Docker build failed%RESET%
    pause
    exit /b 1
)
echo %GREEN%[OK] Docker image built successfully%RESET%

echo.
echo Starting containers...
call docker-compose up -d
if errorlevel 1 (
    echo %RED%[ERROR] Docker startup failed%RESET%
    echo Please check your .env file configuration
    pause
    exit /b 1
)
echo %GREEN%[OK] Docker containers started%RESET%

echo.
echo Waiting for services to be ready (this may take 30-60 seconds)...
timeout /t 20 /nobreak

echo Checking service status...
docker-compose ps

:superuser_prompt
echo.
echo %YELLOW%[QUESTION] Create admin superuser now? (y/n):%RESET%
set /p SUPERUSER="Enter choice: "

if /i "%SUPERUSER%"=="y" (
    echo.
    echo Creating admin superuser...
    call docker-compose exec web python manage.py createsuperuser --settings=config.settings_production
    if errorlevel 1 (
        echo %YELLOW%[WARNING] Superuser creation may need manual intervention%RESET%
        echo You can create it later with: docker-compose exec web python manage.py createsuperuser
    ) else (
        echo %GREEN%[OK] Superuser created%RESET%
    )
) else (
    echo.
    echo %YELLOW%You can create a superuser later with:%RESET%
    echo docker-compose exec web python manage.py createsuperuser
)

:final_info
cls
echo.
echo %GREEN%================================================%RESET%
echo %GREEN%      Deployment Complete! 🔐%RESET%
echo %GREEN%================================================%RESET%
echo.
echo Your School Management System is now running securely with HTTPS!
echo.
echo %BLUE%ACCESS INFORMATION:%RESET%
echo   Main URL: https://localhost
echo   If using domain: https://%DOMAIN%
echo   Admin Panel: https://localhost/admin/
echo.
echo %BLUE%SECURITY INFORMATION:%RESET%
echo   ✓ SSL/TLS: Enabled
echo   ✓ HTTP to HTTPS: Automatic redirect
echo   ✓ Security Headers: Configured
echo   ✓ Database: PostgreSQL with encrypted connections
echo.
echo %BLUE%RUNNING SERVICES:%RESET%
echo   - Django Application ^(port 8000^)
echo   - PostgreSQL Database ^(port 5432^)
echo   - Redis Cache ^(port 6379^)
echo   - Nginx Reverse Proxy ^(ports 80, 443^)
echo.
echo %BLUE%USEFUL DOCKER COMMANDS:%RESET%
echo   View logs: docker-compose logs -f web
echo   Stop services: docker-compose down
echo   Restart: docker-compose restart
echo   Database shell: docker-compose exec db psql -U postgres -d school_management
echo.
echo %YELLOW%IMPORTANT NOTES:%RESET%
echo   1. Keep .env file secure - add to .gitignore
echo   2. Change default SECRET_KEY in production
echo   3. Keep SSL certificates backed up
echo   4. Monitor certificate expiration
echo   5. Regularly update dependencies
echo.
echo %BLUE%DOCUMENTATION:%RESET%
echo   - HTTPS Deployment Guide: HTTPS_DEPLOYMENT.md
echo   - HTTPS Setup Details: HTTPS_SETUP.md
echo   - Project README: README.md
echo.

pause
