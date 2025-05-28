#!/usr/bin/env python3
"""
Docker Security Validation Script
Validates security hardening of Instagram automation Docker containers
"""

import subprocess
import json
import sys
import re
from pathlib import Path

class DockerSecurityValidator:
    def __init__(self):
        self.image_name = "instagram-automation-api:latest"
        self.container_name = "instagram_automation_api"
        self.security_score = 0
        self.max_score = 100
        
    def run_command(self, command, capture_output=True):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=capture_output, 
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_dockerfile_security(self):
        """Validate Dockerfile security practices"""
        print("🔍 Checking Dockerfile security...")
        
        dockerfile_path = Path("Dockerfile.mock-api")
        if not dockerfile_path.exists():
            print("❌ Dockerfile.mock-api not found")
            return 0
        
        content = dockerfile_path.read_text()
        score = 0
        
        # Check for non-root user
        if "USER appuser" in content:
            print("✅ Non-root user configured")
            score += 15
        else:
            print("❌ Running as root user")
        
        # Check for specific version pinning
        if re.search(r"python:3\.11\.\d+-slim-bookworm", content):
            print("✅ Specific base image version pinned")
            score += 10
        else:
            print("❌ Base image version not pinned")
        
        # Check for tini init system
        if "tini" in content:
            print("✅ Tini init system configured")
            score += 10
        else:
            print("❌ No init system configured")
        
        # Check for security labels
        if "LABEL" in content and "maintainer" in content:
            print("✅ Security labels present")
            score += 5
        else:
            print("❌ Missing security labels")
        
        # Check for proper file permissions
        if "--chown=appuser:appuser" in content:
            print("✅ Proper file ownership configured")
            score += 10
        else:
            print("❌ File ownership not configured")
        
        return score
    
    def check_image_vulnerabilities(self):
        """Check for known vulnerabilities in the image"""
        print("\n🔍 Checking image vulnerabilities...")
        
        # Check if image exists
        success, output, error = self.run_command(f"docker images {self.image_name}")
        if not success or self.image_name not in output:
            print("❌ Image not found - build the image first")
            return 0
        
        score = 0
        
        # Try Docker Scout (if available)
        success, output, error = self.run_command(f"docker scout cves {self.image_name}")
        if success:
            if "No vulnerabilities found" in output or "0 vulnerabilities" in output:
                print("✅ No critical vulnerabilities found")
                score += 20
            else:
                print("⚠️ Some vulnerabilities found - check Docker Scout output")
                score += 10
        else:
            print("ℹ️ Docker Scout not available - manual vulnerability check needed")
            score += 5
        
        return score
    
    def check_container_security(self):
        """Check running container security"""
        print("\n🔍 Checking container security...")
        
        # Check if container is running
        success, output, error = self.run_command(f"docker ps --filter name={self.container_name}")
        if not success or self.container_name not in output:
            print("ℹ️ Container not running - starting for security check...")
            self.run_command(f"docker run -d --name {self.container_name}_test {self.image_name}")
            container_name = f"{self.container_name}_test"
        else:
            container_name = self.container_name
        
        score = 0
        
        # Check user
        success, output, error = self.run_command(f"docker exec {container_name} whoami")
        if success and "appuser" in output:
            print("✅ Container running as non-root user")
            score += 15
        else:
            print("❌ Container running as root")
        
        # Check file permissions
        success, output, error = self.run_command(f"docker exec {container_name} ls -la /app")
        if success and "appuser appuser" in output:
            print("✅ Proper file ownership in container")
            score += 10
        else:
            print("❌ Incorrect file ownership")
        
        # Check for writable directories
        success, output, error = self.run_command(f"docker exec {container_name} find /app -type d -writable")
        if success:
            writable_dirs = [line for line in output.split('\n') if line.strip()]
            if len(writable_dirs) <= 2:  # Only /app/data and /app/logs should be writable
                print("✅ Minimal writable directories")
                score += 10
            else:
                print("⚠️ Too many writable directories")
                score += 5
        
        # Cleanup test container
        if container_name.endswith("_test"):
            self.run_command(f"docker rm -f {container_name}")
        
        return score
    
    def check_dockerignore(self):
        """Check .dockerignore security"""
        print("\n🔍 Checking .dockerignore security...")
        
        dockerignore_path = Path(".dockerignore")
        if not dockerignore_path.exists():
            print("❌ .dockerignore file missing")
            return 0
        
        content = dockerignore_path.read_text()
        score = 0
        
        security_patterns = [
            (".env", "Environment files"),
            ("*.key", "Private keys"),
            ("*.pem", "Certificates"),
            (".git/", "Git repository"),
            ("*.log", "Log files"),
            ("__pycache__/", "Python cache"),
        ]
        
        for pattern, description in security_patterns:
            if pattern in content:
                print(f"✅ {description} excluded")
                score += 3
            else:
                print(f"❌ {description} not excluded")
        
        return score
    
    def check_requirements_security(self):
        """Check requirements.txt security"""
        print("\n🔍 Checking requirements.txt security...")
        
        requirements_path = Path("requirements.txt")
        if not requirements_path.exists():
            print("❌ requirements.txt not found")
            return 0
        
        content = requirements_path.read_text()
        score = 0
        
        # Check for pinned versions
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        pinned_count = sum(1 for line in lines if '==' in line)
        
        if pinned_count >= len(lines) * 0.8:  # 80% or more pinned
            print("✅ Most dependencies pinned to specific versions")
            score += 15
        else:
            print("❌ Dependencies not properly pinned")
        
        # Check for security-related packages
        security_packages = ['cryptography', 'certifi', 'urllib3', 'flask-talisman', 'flask-limiter']
        found_security = sum(1 for pkg in security_packages if pkg in content)
        
        if found_security >= 3:
            print("✅ Security packages included")
            score += 10
        else:
            print("⚠️ Consider adding more security packages")
            score += 5
        
        return score
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n" + "="*60)
        print("🛡️ DOCKER SECURITY VALIDATION REPORT")
        print("="*60)
        
        # Run all security checks
        dockerfile_score = self.check_dockerfile_security()
        vulnerability_score = self.check_image_vulnerabilities()
        container_score = self.check_container_security()
        dockerignore_score = self.check_dockerignore()
        requirements_score = self.check_requirements_security()
        
        total_score = dockerfile_score + vulnerability_score + container_score + dockerignore_score + requirements_score
        
        print(f"\n📊 SECURITY SCORES:")
        print(f"   • Dockerfile Security: {dockerfile_score}/50")
        print(f"   • Vulnerability Check: {vulnerability_score}/20")
        print(f"   • Container Security: {container_score}/35")
        print(f"   • .dockerignore: {dockerignore_score}/18")
        print(f"   • Requirements: {requirements_score}/25")
        print(f"   • TOTAL SCORE: {total_score}/{self.max_score + 48}")
        
        # Calculate percentage
        percentage = (total_score / (self.max_score + 48)) * 100
        
        print(f"\n🎯 SECURITY RATING: {percentage:.1f}%")
        
        if percentage >= 90:
            print("🏆 EXCELLENT - Enterprise-grade security!")
            grade = "A+"
        elif percentage >= 80:
            print("✅ GOOD - Strong security posture")
            grade = "A"
        elif percentage >= 70:
            print("⚠️ FAIR - Some security improvements needed")
            grade = "B"
        elif percentage >= 60:
            print("❌ POOR - Significant security issues")
            grade = "C"
        else:
            print("🚨 CRITICAL - Major security vulnerabilities")
            grade = "F"
        
        print(f"📝 GRADE: {grade}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if percentage < 90:
            print("   • Review failed security checks above")
            print("   • Update to latest secure package versions")
            print("   • Implement missing security controls")
        
        if percentage >= 80:
            print("   • Consider implementing runtime security monitoring")
            print("   • Set up automated vulnerability scanning")
            print("   • Regular security audits recommended")
        
        print("\n🔗 RESOURCES:")
        print("   • Docker Security Guide: ./DOCKER_SECURITY_GUIDE.md")
        print("   • OWASP Container Security: https://owasp.org/www-project-container-security/")
        print("   • CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker")
        
        return percentage >= 80

def main():
    """Main function"""
    print("🛡️ Docker Security Validation for Instagram Automation")
    print("=" * 60)
    
    validator = DockerSecurityValidator()
    
    try:
        success = validator.generate_security_report()
        
        if success:
            print("\n🎉 Security validation passed!")
            sys.exit(0)
        else:
            print("\n⚠️ Security improvements needed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Security validation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during security validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
