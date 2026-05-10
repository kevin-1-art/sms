#!/bin/bash

# School Management System - Secure HTTPS Deployment Setup Script
# This script automates the setup of SSL certificates and Docker deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions for colored output
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Install from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Install from: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Create .env file
setup_env_file() {
    print_header "Setting Up Environment File"
    
    if [ -f .env ]; then
        print_warning ".env file already exists. Skipping..."
        return
    fi
    
    if [ ! -f .env.example ]; then
        print_error ".env.example not found. Make sure you're in the project root directory."
        exit 1
    fi
    
    # Copy template
    cp .env.example .env
    print_success ".env file created"
    
    # Generate SECRET_KEY
    echo ""
    echo "Generating Django SECRET_KEY..."
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 2>/dev/null || echo "change-me-in-production-$(date +%s)")
    
    # Update .env with SECRET_KEY
    if command -v sed &> /dev/null; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        else
            # Linux
            sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        fi
        print_success "SECRET_KEY generated and saved"
    fi
    
    # Prompt for user input
    echo ""
    echo -e "${YELLOW}Please enter your configuration:${NC}"
    read -p "Domain name (e.g., yourdomain.com): " DOMAIN
    read -p "Email for SSL certificate: " EMAIL
    read -p "Database password (strong password recommended): " DB_PASSWORD
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN/" .env
        sed -i '' "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" .env
        sed -i '' "s/^DEFAULT_FROM_EMAIL=.*/DEFAULT_FROM_EMAIL=noreply@$DOMAIN/" .env
    else
        sed -i "s/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN/" .env
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" .env
        sed -i "s/^DEFAULT_FROM_EMAIL=.*/DEFAULT_FROM_EMAIL=noreply@$DOMAIN/" .env
    fi
    
    print_success "Environment variables configured"
}

# Generate SSL certificates
setup_ssl_certificates() {
    print_header "Setting Up SSL Certificates"
    
    # Create certs directory
    mkdir -p certs
    
    if [ -f certs/cert.pem ] && [ -f certs/key.pem ]; then
        print_warning "SSL certificates already exist. Skipping..."
        return
    fi
    
    echo ""
    echo -e "${YELLOW}SSL Certificate Options:${NC}"
    echo "1) Self-signed certificate (Development/Testing)"
    echo "2) Let's Encrypt certificate (Production - requires domain)"
    read -p "Choose option (1 or 2): " CERT_OPTION
    
    case $CERT_OPTION in
        1)
            print_header "Generating Self-Signed Certificate"
            openssl req -x509 -newkey rsa:4096 -nodes \
                -out certs/cert.pem \
                -keyout certs/key.pem \
                -days 365 \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
            print_success "Self-signed certificate generated"
            print_warning "Note: Self-signed certificates show warnings in browsers"
            ;;
        2)
            print_header "Let's Encrypt Certificate Setup"
            
            # Check if certbot is installed
            if ! command -v certbot &> /dev/null; then
                print_warning "Certbot is not installed. Installing..."
                if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                    sudo apt-get update
                    sudo apt-get install -y certbot
                elif [[ "$OSTYPE" == "darwin"* ]]; then
                    brew install certbot
                fi
            fi
            
            read -p "Enter your domain name: " DOMAIN
            read -p "Enter your email address: " EMAIL
            
            echo "Generating Let's Encrypt certificate for $DOMAIN..."
            echo "Note: This requires your domain to be accessible from the internet"
            
            if certbot certonly --standalone -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos -n; then
                # Copy certificates to project
                sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" certs/cert.pem
                sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" certs/key.pem
                sudo chown $USER:$USER certs/*
                print_success "Let's Encrypt certificate configured"
            else
                print_error "Let's Encrypt certificate generation failed"
                print_warning "Generating self-signed certificate as fallback..."
                openssl req -x509 -newkey rsa:4096 -nodes \
                    -out certs/cert.pem \
                    -keyout certs/key.pem \
                    -days 365 \
                    -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
                print_warning "Fallback to self-signed certificate complete"
            fi
            ;;
        *)
            print_error "Invalid option. Using self-signed certificate."
            openssl req -x509 -newkey rsa:4096 -nodes \
                -out certs/cert.pem \
                -keyout certs/key.pem \
                -days 365 \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
            ;;
    esac
    
    # Verify certificates
    if [ -f certs/cert.pem ] && [ -f certs/key.pem ]; then
        print_success "SSL certificates are ready"
    else
        print_error "SSL certificate setup failed"
        exit 1
    fi
}

# Build and start Docker containers
start_docker_containers() {
    print_header "Starting Docker Containers"
    
    echo "Building Docker image..."
    if docker-compose build; then
        print_success "Docker image built successfully"
    else
        print_error "Docker build failed"
        exit 1
    fi
    
    echo ""
    echo "Starting containers..."
    if docker-compose up -d; then
        print_success "Docker containers started"
    else
        print_error "Docker startup failed"
        exit 1
    fi
    
    # Wait for services to be healthy
    echo ""
    echo "Waiting for services to be ready (this may take 30-60 seconds)..."
    sleep 15
    
    # Check if services are healthy
    echo "Checking service status..."
    if docker-compose ps | grep -q "healthy"; then
        print_success "All services are healthy"
    else
        print_warning "Some services may still be starting. Check with: docker-compose ps"
    fi
}

# Create superuser
create_superuser() {
    print_header "Creating Admin User"
    
    echo ""
    echo -e "${YELLOW}Create a superuser account for admin panel:${NC}"
    docker-compose exec web python manage.py createsuperuser \
        --settings=config.settings_production
    
    print_success "Superuser created"
}

# Display final information
display_info() {
    print_header "Deployment Complete!"
    
    echo ""
    echo -e "${GREEN}Your School Management System is now running securely with HTTPS! 🔐${NC}"
    echo ""
    echo "📋 Access Information:"
    echo "  Main URL: https://localhost (or your domain)"
    echo "  Admin Panel: https://localhost/admin/"
    echo ""
    echo "🔐 Security Information:"
    echo "  SSL/TLS: Enabled"
    echo "  HTTP to HTTPS: Automatic redirect"
    echo "  Security Headers: Configured"
    echo "  Database: PostgreSQL with encrypted connections"
    echo ""
    echo "📊 Running Services:"
    echo "  - Django Application (port 8000)"
    echo "  - PostgreSQL Database (port 5432)"
    echo "  - Redis Cache (port 6379)"
    echo "  - Nginx Reverse Proxy (ports 80, 443)"
    echo ""
    echo "🛠️ Useful Docker Commands:"
    echo "  View logs: docker-compose logs -f web"
    echo "  Stop services: docker-compose down"
    echo "  Restart: docker-compose restart"
    echo "  Database shell: docker-compose exec db psql -U postgres -d school_management"
    echo ""
    echo "📚 Documentation:"
    echo "  Deployment Guide: https://github.com/your-repo/HTTPS_DEPLOYMENT.md"
    echo "  HTTPS Setup: https://github.com/your-repo/HTTPS_SETUP.md"
    echo ""
    echo -e "${YELLOW}⚠️  Important Notes:${NC}"
    echo "  1. Keep .env file secure - add to .gitignore"
    echo "  2. Change default SECRET_KEY in production"
    echo "  3. Keep SSL certificates backed up"
    echo "  4. Monitor certificate expiration"
    echo "  5. Regularly update dependencies"
    echo ""
}

# Main execution
main() {
    clear
    print_header "School Management System - HTTPS Deployment Setup"
    echo ""
    echo "This script will setup and deploy the system securely with HTTPS."
    echo ""
    
    check_prerequisites
    setup_env_file
    setup_ssl_certificates
    start_docker_containers
    
    # Ask if user wants to create superuser now
    echo ""
    read -p "Create admin superuser now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_superuser
    fi
    
    display_info
}

# Run main function
main
