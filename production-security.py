#!/usr/bin/env python3
"""
Production Security Configuration
Additional security measures for production deployment
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta

class ProductionSecurity:
    """Production security configuration and utilities"""
    
    @staticmethod
    def generate_secure_secret_key():
        """Generate cryptographically secure secret key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_api_key():
        """Generate secure API key for authentication"""
        timestamp = datetime.now().isoformat()
        random_data = secrets.token_bytes(32)
        combined = f"{timestamp}{random_data.hex()}".encode()
        return hashlib.sha256(combined).hexdigest()
    
    @staticmethod
    def get_security_headers():
        """Get comprehensive security headers for production"""
        return {
            # XSS Protection
            'X-XSS-Protection': '1; mode=block',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            
            # HTTPS Security
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            'Upgrade-Insecure-Requests': '1',
            
            # Content Security Policy
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "font-src 'self'; "
                "object-src 'none'; "
                "media-src 'self'; "
                "frame-src 'none'; "
                "worker-src 'none'; "
                "manifest-src 'self';"
            ),
            
            # Privacy and Security
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': (
                'geolocation=(), microphone=(), camera=(), '
                'payment=(), usb=(), magnetometer=(), gyroscope=()'
            ),
            
            # Cache Control
            'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            
            # Additional Security
            'X-Permitted-Cross-Domain-Policies': 'none',
            'Cross-Origin-Embedder-Policy': 'require-corp',
            'Cross-Origin-Opener-Policy': 'same-origin',
            'Cross-Origin-Resource-Policy': 'same-origin'
        }
    
    @staticmethod
    def get_secure_flask_config():
        """Get secure Flask configuration for production"""
        return {
            # Session Security
            'SECRET_KEY': ProductionSecurity.generate_secure_secret_key(),
            'SESSION_COOKIE_SECURE': True,
            'SESSION_COOKIE_HTTPONLY': True,
            'SESSION_COOKIE_SAMESITE': 'Strict',
            'PERMANENT_SESSION_LIFETIME': timedelta(hours=1),
            
            # Security Settings
            'WTF_CSRF_ENABLED': True,
            'WTF_CSRF_TIME_LIMIT': 3600,
            'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
            'SEND_FILE_MAX_AGE_DEFAULT': 0,
            
            # JSON Security
            'JSON_SORT_KEYS': False,
            'JSONIFY_PRETTYPRINT_REGULAR': False,
            'JSONIFY_MIMETYPE': 'application/json',
            
            # Upload Security
            'UPLOAD_FOLDER': '/app/data/uploads',
            'ALLOWED_EXTENSIONS': {'txt', 'json', 'csv'},
            
            # Rate Limiting
            'RATELIMIT_STORAGE_URL': 'memory://',
            'RATELIMIT_DEFAULT': '100 per hour',
            'RATELIMIT_HEADERS_ENABLED': True,
        }
    
    @staticmethod
    def validate_environment():
        """Validate production environment security"""
        required_vars = [
            'FLASK_ENV',
            'SECRET_KEY',
            'NGROK_AUTHTOKEN'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")
        
        # Validate Flask environment
        if os.getenv('FLASK_ENV') != 'production':
            raise ValueError("FLASK_ENV must be set to 'production'")
        
        return True
    
    @staticmethod
    def get_logging_config():
        """Get secure logging configuration"""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'security': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
                'json': {
                    'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
                }
            },
            'handlers': {
                'file': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': '/app/logs/security.log',
                    'formatter': 'security'
                },
                'console': {
                    'level': 'WARNING',
                    'class': 'logging.StreamHandler',
                    'formatter': 'json'
                }
            },
            'loggers': {
                'security': {
                    'handlers': ['file', 'console'],
                    'level': 'INFO',
                    'propagate': False
                }
            }
        }

# Security constants
SECURITY_CONSTANTS = {
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION': 900,  # 15 minutes
    'SESSION_TIMEOUT': 3600,  # 1 hour
    'API_RATE_LIMIT': 100,    # requests per hour
    'MAX_FILE_SIZE': 16 * 1024 * 1024,  # 16MB
    'ALLOWED_ORIGINS': ['http://localhost:5678'],
    'SECURE_HEADERS_REQUIRED': True,
    'FORCE_HTTPS': True,
    'CSRF_PROTECTION': True
}

# Export for use in main application
__all__ = [
    'ProductionSecurity',
    'SECURITY_CONSTANTS'
]
