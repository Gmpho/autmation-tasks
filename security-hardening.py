#!/usr/bin/env python3
"""
Security Hardening Script for Instagram Automation
Implements comprehensive security measures to prevent all types of injections
"""

import os
import re
import html
import logging
from typing import Any, Dict
from functools import wraps

# Security dependencies - all required packages
import bleach
import validators
from flask import request, abort
from werkzeug.exceptions import BadRequest

# Configure secure logging
try:
    # Try to create logs directory if it doesn't exist
    os.makedirs('/app/logs', exist_ok=True)
    log_handlers = [
        logging.FileHandler('/app/logs/security.log'),
        logging.StreamHandler()
    ]
except (OSError, PermissionError):
    # Fallback to console only if file logging fails
    log_handlers = [logging.StreamHandler()]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

class SecurityHardening:
    """Comprehensive security hardening class"""

    # Allowed HTML tags for content sanitization
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
    ALLOWED_ATTRIBUTES = {}

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"].*['\"])",
        r"(;|\|\||&&)",
    ]

    # XSS patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"onclick\s*=",
        r"onmouseover\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
    ]

    # Command injection patterns
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$(){}[\]\\]",
        r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat|ifconfig|ping|wget|curl|nc|telnet|ssh|ftp)\b",
        r"(\.\.\/|\.\.\\)",
        r"(/etc/passwd|/etc/shadow|/proc/|/sys/)",
    ]

    # Path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        r"(\.\.\/|\.\.\\)",
        r"(%2e%2e%2f|%2e%2e%5c)",
        r"(\.\.%2f|\.\.%5c)",
        r"(%252e%252e%252f|%252e%252e%255c)",
    ]

    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """Sanitize input data to prevent injections"""
        if isinstance(data, str):
            return SecurityHardening._sanitize_string(data)
        elif isinstance(data, dict):
            return {k: SecurityHardening.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityHardening.sanitize_input(item) for item in data]
        else:
            return data

    @staticmethod
    def _sanitize_string(text: str) -> str:
        """Sanitize string input"""
        if not isinstance(text, str):
            return text

        # HTML escape
        text = html.escape(text)

        # HTML sanitization with bleach
        text = bleach.clean(
            text,
            tags=SecurityHardening.ALLOWED_TAGS,
            attributes=SecurityHardening.ALLOWED_ATTRIBUTES,
            strip=True
        )

        # Remove null bytes
        text = text.replace('\x00', '')

        # Limit length to prevent DoS
        if len(text) > 10000:
            text = text[:10000]
            logger.warning(f"Input truncated due to length: {len(text)}")

        return text

    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """Detect SQL injection attempts"""
        text_lower = text.lower()
        for pattern in SecurityHardening.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning(f"SQL injection attempt detected: {pattern}")
                return True
        return False

    @staticmethod
    def detect_xss(text: str) -> bool:
        """Detect XSS attempts"""
        text_lower = text.lower()
        for pattern in SecurityHardening.XSS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning(f"XSS attempt detected: {pattern}")
                return True
        return False

    @staticmethod
    def detect_command_injection(text: str) -> bool:
        """Detect command injection attempts"""
        for pattern in SecurityHardening.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Command injection attempt detected: {pattern}")
                return True
        return False

    @staticmethod
    def detect_path_traversal(text: str) -> bool:
        """Detect path traversal attempts"""
        for pattern in SecurityHardening.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Path traversal attempt detected: {pattern}")
                return True
        return False

    @staticmethod
    def validate_input(data: Any) -> bool:
        """Comprehensive input validation"""
        if isinstance(data, str):
            # Check for various injection types
            if (SecurityHardening.detect_sql_injection(data) or
                SecurityHardening.detect_xss(data) or
                SecurityHardening.detect_command_injection(data) or
                SecurityHardening.detect_path_traversal(data)):
                return False
        elif isinstance(data, dict):
            for key, value in data.items():
                if not SecurityHardening.validate_input(key) or not SecurityHardening.validate_input(value):
                    return False
        elif isinstance(data, list):
            for item in data:
                if not SecurityHardening.validate_input(item):
                    return False

        return True

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format and security"""
        # Validate URL format
        if not validators.url(url):
            return False

        # Check for dangerous protocols
        dangerous_protocols = ['javascript:', 'vbscript:', 'data:', 'file:']
        url_lower = url.lower()
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                logger.warning(f"Dangerous protocol detected: {protocol}")
                return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        return validators.email(email)

    @staticmethod
    def secure_headers() -> Dict[str, str]:
        """Generate secure HTTP headers"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; media-src 'self'; frame-src 'none';",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }

def security_middleware(f):
    """Security middleware decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log request for security monitoring
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

        # Validate request data
        if request.is_json:
            try:
                data = request.get_json()
                if data and not SecurityHardening.validate_input(data):
                    logger.warning(f"Malicious input detected from {request.remote_addr}")
                    abort(400, description="Invalid input detected")
            except BadRequest:
                logger.warning(f"Invalid JSON from {request.remote_addr}")
                abort(400, description="Invalid JSON")

        # Validate query parameters
        for key, value in request.args.items():
            if not SecurityHardening.validate_input(key) or not SecurityHardening.validate_input(value):
                logger.warning(f"Malicious query parameter detected from {request.remote_addr}")
                abort(400, description="Invalid query parameter")

        # Execute the original function
        response = f(*args, **kwargs)

        # Add security headers
        if hasattr(response, 'headers'):
            for header, value in SecurityHardening.secure_headers().items():
                response.headers[header] = value

        return response

    return decorated_function

def rate_limit_middleware():
    """Rate limiting middleware"""
    # This would integrate with Flask-Limiter
    pass

def input_sanitizer(data: Any) -> Any:
    """Public function to sanitize input data"""
    return SecurityHardening.sanitize_input(data)

def validate_api_input(data: Any) -> bool:
    """Public function to validate API input"""
    return SecurityHardening.validate_input(data)

# Security configuration for Flask app
SECURITY_CONFIG = {
    'SECRET_KEY': os.urandom(32),
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Strict',
    'PERMANENT_SESSION_LIFETIME': 3600,  # 1 hour
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max
    'SEND_FILE_MAX_AGE_DEFAULT': 0,
    'JSONIFY_PRETTYPRINT_REGULAR': False,
}

# Export security functions
__all__ = [
    'SecurityHardening',
    'security_middleware',
    'input_sanitizer',
    'validate_api_input',
    'SECURITY_CONFIG'
]
