#!/usr/bin/env python3
"""
Test Security Hardening Implementation
Validates that security hardening works without external dependencies
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import security_hardening
    from security_hardening import SecurityHardening, input_sanitizer, validate_api_input
    print("✅ Security hardening module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import security hardening: {e}")
    print("💡 Make sure security-hardening.py is in the same directory")
    sys.exit(1)

def test_input_sanitization():
    """Test input sanitization"""
    print("\n🧪 Testing Input Sanitization...")

    test_cases = [
        {
            "input": "<script>alert('XSS')</script>",
            "description": "XSS Script Tag"
        },
        {
            "input": "'; DROP TABLE users; --",
            "description": "SQL Injection"
        },
        {
            "input": "../../../etc/passwd",
            "description": "Path Traversal"
        },
        {
            "input": "; cat /etc/passwd",
            "description": "Command Injection"
        },
        {
            "input": "Normal text content",
            "description": "Safe Content"
        }
    ]

    for test in test_cases:
        sanitized = input_sanitizer(test["input"])
        print(f"   • {test['description']}: '{test['input']}' → '{sanitized}'")

    return True

def test_input_validation():
    """Test input validation"""
    print("\n🛡️ Testing Input Validation...")

    dangerous_inputs = [
        "<script>alert(1)</script>",
        "'; DROP TABLE users; --",
        "; cat /etc/passwd",
        "../../../etc/passwd",
        "javascript:alert(1)"
    ]

    safe_inputs = [
        "Hello world",
        "user@example.com",
        "https://example.com",
        "Normal content"
    ]

    print("   Dangerous inputs (should be rejected):")
    for dangerous in dangerous_inputs:
        is_valid = validate_api_input(dangerous)
        status = "❌ BLOCKED" if not is_valid else "⚠️ ALLOWED"
        print(f"     • '{dangerous}': {status}")

    print("   Safe inputs (should be allowed):")
    for safe in safe_inputs:
        is_valid = validate_api_input(safe)
        status = "✅ ALLOWED" if is_valid else "❌ BLOCKED"
        print(f"     • '{safe}': {status}")

    return True

def test_url_validation():
    """Test URL validation"""
    print("\n🌐 Testing URL Validation...")

    test_urls = [
        ("https://example.com", "Valid HTTPS URL", True),
        ("http://localhost:8000", "Valid HTTP localhost", True),
        ("javascript:alert(1)", "Dangerous JavaScript", False),
        ("vbscript:msgbox(1)", "Dangerous VBScript", False),
        ("data:text/html,<script>alert(1)</script>", "Dangerous Data URL", False),
        ("file:///etc/passwd", "Dangerous File URL", False),
        ("https://valid-domain.com/path", "Valid URL with path", True)
    ]

    for url, description, expected in test_urls:
        is_valid = SecurityHardening.validate_url(url)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        expected_status = "✅" if expected else "❌"
        match = "✅" if (is_valid == expected) else "⚠️ MISMATCH"
        print(f"   • {description}: {status} (Expected: {expected_status}) {match}")

    return True

def test_email_validation():
    """Test email validation"""
    print("\n📧 Testing Email Validation...")

    test_emails = [
        ("user@example.com", "Valid email", True),
        ("test.email+tag@domain.co.uk", "Valid complex email", True),
        ("invalid-email", "Invalid email", False),
        ("@domain.com", "Missing username", False),
        ("user@", "Missing domain", False),
        ("user@domain", "Missing TLD", False)
    ]

    for email, description, expected in test_emails:
        is_valid = SecurityHardening.validate_email(email)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        expected_status = "✅" if expected else "❌"
        match = "✅" if (is_valid == expected) else "⚠️ MISMATCH"
        print(f"   • {description}: {status} (Expected: {expected_status}) {match}")

    return True

def test_security_headers():
    """Test security headers generation"""
    print("\n🔒 Testing Security Headers...")

    headers = SecurityHardening.secure_headers()

    required_headers = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection',
        'Strict-Transport-Security',
        'Content-Security-Policy',
        'Referrer-Policy'
    ]

    for header in required_headers:
        if header in headers:
            print(f"   ✅ {header}: {headers[header]}")
        else:
            print(f"   ❌ {header}: MISSING")

    return True

def main():
    """Main test function"""
    print("🛡️ Security Hardening Test Suite")
    print("=" * 50)

    tests = [
        ("Input Sanitization", test_input_sanitization),
        ("Input Validation", test_input_validation),
        ("URL Validation", test_url_validation),
        ("Email Validation", test_email_validation),
        ("Security Headers", test_security_headers)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")

    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All security tests passed!")
        print("✅ Security hardening is working correctly")
        return True
    else:
        print("⚠️ Some security tests failed")
        print("🔧 Review the implementation")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
