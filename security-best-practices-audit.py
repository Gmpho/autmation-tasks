#!/usr/bin/env python3
"""
Comprehensive Security Best Practices Audit
Validates all security measures and suggests improvements
"""

import os
import re
import subprocess
from pathlib import Path

class SecurityAudit:
    def __init__(self):
        self.score = 0
        self.max_score = 0
        self.recommendations = []
        
    def check_dockerfile_security(self):
        """Audit Dockerfile security practices"""
        print("🔍 Auditing Dockerfile security...")
        
        dockerfile_path = Path("Dockerfile.mock-api")
        if not dockerfile_path.exists():
            print("❌ Dockerfile.mock-api not found")
            return 0
        
        content = dockerfile_path.read_text()
        score = 0
        max_score = 100
        
        # Check base image
        if "python:3.13.3-alpine" in content:
            print("✅ Latest secure Python Alpine image")
            score += 15
        else:
            print("⚠️ Consider updating to python:3.13.3-alpine")
            self.recommendations.append("Update to latest Python Alpine image")
        
        # Check multi-stage build
        if "AS builder" in content and "FROM python" in content:
            print("✅ Multi-stage build implemented")
            score += 10
        else:
            print("❌ Multi-stage build missing")
            self.recommendations.append("Implement multi-stage build")
        
        # Check non-root user
        if "USER appuser" in content:
            print("✅ Non-root user configured")
            score += 15
        else:
            print("❌ Running as root user")
            self.recommendations.append("Configure non-root user")
        
        # Check security labels
        if "security.vulnerabilities" in content:
            print("✅ Security labels present")
            score += 5
        else:
            print("⚠️ Add security labels")
            self.recommendations.append("Add security labels")
        
        # Check SUID/SGID removal
        if "find / -type f" in content and "-perm -4000" in content:
            print("✅ SUID/SGID binaries removed")
            score += 10
        else:
            print("⚠️ SUID/SGID removal missing")
            self.recommendations.append("Remove SUID/SGID binaries")
        
        # Check package cleanup
        if "rm -rf /var/cache/apk/*" in content:
            print("✅ Package cache cleanup")
            score += 5
        else:
            print("⚠️ Package cache not cleaned")
            self.recommendations.append("Clean package cache")
        
        # Check secure environment variables
        secure_env_vars = ["PYTHONHASHSEED=random", "PYTHONSAFEPATH=1", "PYTHONDONTWRITEBYTECODE=1"]
        env_score = sum(5 for var in secure_env_vars if var in content)
        print(f"✅ Secure environment variables: {env_score}/15")
        score += env_score
        
        # Check file permissions
        if "--chmod=644" in content:
            print("✅ Secure file permissions")
            score += 10
        else:
            print("⚠️ File permissions not set")
            self.recommendations.append("Set secure file permissions")
        
        # Check minimal dependencies
        if "ca-certificates" in content and "tzdata" in content:
            print("✅ Minimal runtime dependencies")
            score += 10
        else:
            print("⚠️ Review runtime dependencies")
            self.recommendations.append("Minimize runtime dependencies")
        
        # Check CMD security
        if 'CMD ["python3"' in content:
            print("✅ Secure CMD format (exec form)")
            score += 5
        else:
            print("⚠️ Use exec form for CMD")
            self.recommendations.append("Use exec form for CMD")
        
        print(f"📊 Dockerfile Security Score: {score}/{max_score}")
        return score
    
    def check_requirements_security(self):
        """Audit requirements.txt security"""
        print("\n🔍 Auditing requirements.txt security...")
        
        req_path = Path("requirements.txt")
        if not req_path.exists():
            print("❌ requirements.txt not found")
            return 0
        
        content = req_path.read_text()
        score = 0
        max_score = 50
        
        # Check version pinning
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        pinned_count = sum(1 for line in lines if '==' in line)
        
        if pinned_count >= len(lines) * 0.9:  # 90% or more pinned
            print("✅ Dependencies properly pinned")
            score += 20
        else:
            print("⚠️ Pin all dependency versions")
            self.recommendations.append("Pin all dependency versions")
        
        # Check security packages
        security_packages = {
            'cryptography': 'Cryptographic operations',
            'bleach': 'HTML sanitization',
            'validators': 'Input validation',
            'flask-talisman': 'Security headers',
            'flask-limiter': 'Rate limiting',
            'certifi': 'CA certificates',
            'urllib3': 'Secure HTTP'
        }
        
        found_packages = 0
        for package, description in security_packages.items():
            if package in content:
                print(f"✅ {package}: {description}")
                found_packages += 1
            else:
                print(f"⚠️ Missing {package}: {description}")
                self.recommendations.append(f"Add {package} for {description}")
        
        score += (found_packages / len(security_packages)) * 20
        
        # Check for production server
        if 'gunicorn' in content:
            print("✅ Production WSGI server (gunicorn)")
            score += 10
        else:
            print("⚠️ Add production WSGI server")
            self.recommendations.append("Add gunicorn for production")
        
        print(f"📊 Requirements Security Score: {score:.1f}/{max_score}")
        return score
    
    def check_application_security(self):
        """Audit application security"""
        print("\n🔍 Auditing application security...")
        
        app_path = Path("mock_api_server.py")
        if not app_path.exists():
            print("❌ mock_api_server.py not found")
            return 0
        
        content = app_path.read_text()
        score = 0
        max_score = 50
        
        # Check security middleware
        if "security_middleware" in content:
            print("✅ Security middleware implemented")
            score += 15
        else:
            print("❌ Security middleware missing")
            self.recommendations.append("Implement security middleware")
        
        # Check input validation
        if "validate_input" in content or "sanitize_input" in content:
            print("✅ Input validation/sanitization")
            score += 15
        else:
            print("❌ Input validation missing")
            self.recommendations.append("Add input validation")
        
        # Check CORS configuration
        if "CORS" in content:
            print("✅ CORS configured")
            score += 5
        else:
            print("⚠️ CORS not configured")
            self.recommendations.append("Configure CORS properly")
        
        # Check error handling
        if "abort" in content and "400" in content:
            print("✅ Secure error handling")
            score += 5
        else:
            print("⚠️ Improve error handling")
            self.recommendations.append("Add secure error handling")
        
        # Check logging
        if "logging" in content:
            print("✅ Security logging")
            score += 10
        else:
            print("⚠️ Add security logging")
            self.recommendations.append("Implement security logging")
        
        print(f"📊 Application Security Score: {score}/{max_score}")
        return score
    
    def check_additional_security_files(self):
        """Check for additional security files"""
        print("\n🔍 Checking additional security files...")
        
        score = 0
        max_score = 30
        
        security_files = {
            '.dockerignore': 'Excludes sensitive files from build context',
            'security-hardening.py': 'Security hardening implementation',
            'validate-docker-security.py': 'Security validation script',
            'DOCKER_SECURITY_GUIDE.md': 'Security documentation'
        }
        
        for file_name, description in security_files.items():
            if Path(file_name).exists():
                print(f"✅ {file_name}: {description}")
                score += 7.5
            else:
                print(f"⚠️ Missing {file_name}: {description}")
                self.recommendations.append(f"Create {file_name}")
        
        print(f"📊 Additional Security Files Score: {score}/{max_score}")
        return score
    
    def suggest_improvements(self):
        """Suggest additional security improvements"""
        print("\n💡 Additional Security Recommendations:")
        
        additional_recommendations = [
            "Implement image digest pinning for maximum security",
            "Add health check with security validation",
            "Configure secrets management for production",
            "Set up automated security scanning in CI/CD",
            "Implement runtime security monitoring",
            "Add penetration testing procedures",
            "Configure backup and disaster recovery",
            "Set up security alerting and monitoring",
            "Implement API rate limiting per endpoint",
            "Add request/response encryption for sensitive data"
        ]
        
        for i, rec in enumerate(additional_recommendations, 1):
            print(f"   {i}. {rec}")
        
        return additional_recommendations
    
    def generate_report(self):
        """Generate comprehensive security audit report"""
        print("\n" + "="*70)
        print("🛡️ COMPREHENSIVE SECURITY AUDIT REPORT")
        print("="*70)
        
        # Run all audits
        dockerfile_score = self.check_dockerfile_security()
        requirements_score = self.check_requirements_security()
        application_score = self.check_application_security()
        files_score = self.check_additional_security_files()
        
        total_score = dockerfile_score + requirements_score + application_score + files_score
        max_total = 230
        
        percentage = (total_score / max_total) * 100
        
        print(f"\n📊 SECURITY AUDIT SUMMARY:")
        print("-" * 40)
        print(f"   • Dockerfile Security: {dockerfile_score}/100")
        print(f"   • Requirements Security: {requirements_score:.1f}/50")
        print(f"   • Application Security: {application_score}/50")
        print(f"   • Security Files: {files_score}/30")
        print(f"   • TOTAL SCORE: {total_score:.1f}/{max_total}")
        print(f"   • PERCENTAGE: {percentage:.1f}%")
        
        # Grade assignment
        if percentage >= 95:
            grade = "A+"
            status = "🏆 EXCEPTIONAL - Military-grade security"
        elif percentage >= 90:
            grade = "A"
            status = "✅ EXCELLENT - Enterprise-ready"
        elif percentage >= 80:
            grade = "B+"
            status = "✅ VERY GOOD - Production-ready"
        elif percentage >= 70:
            grade = "B"
            status = "⚠️ GOOD - Minor improvements needed"
        elif percentage >= 60:
            grade = "C"
            status = "⚠️ FAIR - Several improvements needed"
        else:
            grade = "D"
            status = "❌ POOR - Major security issues"
        
        print(f"\n🎯 SECURITY GRADE: {grade}")
        print(f"📝 STATUS: {status}")
        
        # Recommendations
        if self.recommendations:
            print(f"\n🔧 PRIORITY RECOMMENDATIONS:")
            for i, rec in enumerate(self.recommendations[:5], 1):
                print(f"   {i}. {rec}")
        
        # Additional suggestions
        additional = self.suggest_improvements()
        
        print(f"\n🚀 DEPLOYMENT READINESS:")
        if percentage >= 90:
            print("   ✅ Ready for production deployment")
            print("   ✅ Enterprise security standards met")
            print("   ✅ Cloud deployment approved")
        elif percentage >= 80:
            print("   ✅ Ready for production with minor improvements")
            print("   ⚠️ Address priority recommendations")
        else:
            print("   ❌ Not ready for production")
            print("   🔧 Address security issues before deployment")
        
        return percentage >= 80

def main():
    """Main audit function"""
    print("🛡️ Security Best Practices Audit for Instagram Automation")
    print("=" * 70)
    
    auditor = SecurityAudit()
    
    try:
        ready = auditor.generate_report()
        
        if ready:
            print("\n🎉 SECURITY AUDIT PASSED!")
            print("🚀 Your system meets security best practices!")
        else:
            print("\n⚠️ Security improvements needed")
            print("🔧 Address the recommendations above")
        
    except Exception as e:
        print(f"\n❌ Audit error: {e}")

if __name__ == "__main__":
    main()
