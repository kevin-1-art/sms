"""
Landing page view for School Management System
"""
from django.http import HttpResponse
from django.views import View

class LandingPageView(View):
    """Simple landing page without database dependency"""
    
    def get(self, request):
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TSURI - Secure HTTPS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .landing-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            text-align: center;
            max-width: 700px;
            animation: slideUp 0.8s ease;
        }
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .logo-section {
            margin-bottom: 30px;
        }
        .lock-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        h1 {
            color: #333;
            font-weight: 700;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        .https-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            margin-bottom: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .btn-group {
            margin-top: 40px;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 30px;
            font-size: 1em;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            color: white;
            text-decoration: none;
        }
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .btn-secondary:hover {
            background: #667eea;
            color: white;
            text-decoration: none;
        }
        .tech-stack {
            margin-top: 30px;
            color: #999;
            font-size: 0.85em;
        }
        .tech-stack strong {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="landing-container">
        <div class="logo-section">
            <div class="lock-icon">🔒</div>
            <div class="https-badge">✓ HTTPS SECURED</div>
        </div>
        
        <h1>TSURI</h1>
        <p class="subtitle">Secure. Reliable. Modern.</p>
        
        <div class="btn-group">
            <a href="/admin/" class="btn btn-primary">Admin Panel</a>
            <a href="https://securityheaders.com/?q=localhost&followRedirects=on" class="btn btn-secondary" target="_blank">Check Security</a>
        </div>
        
        <div class="tech-stack">
            <strong>Technology Stack:</strong><br>
            Django 4.2 • Bootstrap 5 • PostgreSQL Ready • Docker Ready<br>
            <strong>Deployment:</strong> Docker, Cloud-Ready, HTTPS Enabled
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        return HttpResponse(html, content_type='text/html')
