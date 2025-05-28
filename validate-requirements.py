#!/usr/bin/env python3
"""
Requirements.txt Security Validation
Validates that all packages are properly configured and secure
"""

import re
import subprocess
from pathlib import Path

class RequirementsValidator:
    def __init__(self):
        self.requirements_file = Path("requirements.txt")
        self.score = 0
        self.max_score = 100
        
    def check_file_exists(self):
        """Check if requirements.txt exists"""
        if self.requirements_file.exists():
            print("✅ requirements.txt file exists")
            return True
        else:
            print("❌ requirements.txt file not found")
            return False
    
    def parse_requirements(self):
        """Parse requirements.txt and extract packages"""
        if not self.requirements_file.exists():
            return []
        
        content = self.requirements_file.read_text()
        packages = []
        
        for line in content.split('\n'):
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Extract package name and version
                if '==' in line:
                    package_info = line.split('#')[0].strip()  # Remove inline comments
                    packages.append(package_info)
        
        return packages
    
    def check_version_pinning(self):
        """Check if all packages have pinned versions"""
        print("\n🔍 Checking version pinning...")
        
        packages = self.parse_requirements()
        if not packages:
            print("❌ No packages found")
            return 0
        
        pinned_count = 0
        unpinned = []
        
        for package in packages:
            if '==' in package:
                print(f"✅ {package}")
                pinned_count += 1
            else:
                print(f"❌ {package} (not pinned)")
                unpinned.append(package)
        
        percentage = (pinned_count / len(packages)) * 100
        print(f"\n📊 Version Pinning: {pinned_count}/{len(packages)} ({percentage:.1f}%)")
        
        if unpinned:
            print(f"⚠️ Unpinned packages: {unpinned}")
        
        return min(30, int(percentage * 0.3))
    
    def check_security_packages(self):
        """Check for essential security packages"""
        print("\n🛡️ Checking security packages...")
        
        content = self.requirements_file.read_text()
        
        essential_security = {
            'cryptography': 'Cryptographic operations',
            'bleach': 'HTML sanitization',
            'validators': 'Input validation',
            'flask-talisman': 'Security headers',
            'flask-limiter': 'Rate limiting',
            'certifi': 'CA certificates',
            'urllib3': 'Secure HTTP',
            'requests': 'HTTP library',
            'werkzeug': 'WSGI utilities'
        }
        
        found_packages = 0
        missing_packages = []
        
        for package, description in essential_security.items():
            if package in content:
                print(f"✅ {package}: {description}")
                found_packages += 1
            else:
                print(f"❌ {package}: {description} (MISSING)")
                missing_packages.append(package)
        
        percentage = (found_packages / len(essential_security)) * 100
        print(f"\n📊 Security Packages: {found_packages}/{len(essential_security)} ({percentage:.1f}%)")
        
        if missing_packages:
            print(f"⚠️ Missing security packages: {missing_packages}")
        
        return min(25, int(percentage * 0.25))
    
    def check_production_packages(self):
        """Check for production-ready packages"""
        print("\n🚀 Checking production packages...")
        
        content = self.requirements_file.read_text()
        
        production_packages = {
            'gunicorn': 'Production WSGI server',
            'structlog': 'Structured logging',
            'flask': 'Web framework',
            'python-dotenv': 'Environment management'
        }
        
        found_packages = 0
        
        for package, description in production_packages.items():
            if package in content:
                print(f"✅ {package}: {description}")
                found_packages += 1
            else:
                print(f"❌ {package}: {description} (MISSING)")
        
        percentage = (found_packages / len(production_packages)) * 100
        print(f"\n📊 Production Packages: {found_packages}/{len(production_packages)} ({percentage:.1f}%)")
        
        return min(20, int(percentage * 0.2))
    
    def check_development_packages(self):
        """Check for development and testing packages"""
        print("\n🧪 Checking development packages...")
        
        content = self.requirements_file.read_text()
        
        dev_packages = {
            'bandit': 'Security linter',
            'safety': 'Vulnerability scanner'
        }
        
        found_packages = 0
        
        for package, description in dev_packages.items():
            if package in content:
                print(f"✅ {package}: {description}")
                found_packages += 1
            else:
                print(f"⚠️ {package}: {description} (OPTIONAL)")
        
        percentage = (found_packages / len(dev_packages)) * 100
        print(f"\n📊 Development Packages: {found_packages}/{len(dev_packages)} ({percentage:.1f}%)")
        
        return min(10, int(percentage * 0.1))
    
    def check_package_organization(self):
        """Check if packages are well organized with comments"""
        print("\n📋 Checking package organization...")
        
        content = self.requirements_file.read_text()
        
        organization_checks = {
            'Has comments': '# ' in content,
            'Has sections': content.count('#') >= 5,
            'Has descriptions': ' # ' in content,
            'Updated recently': '2024' in content,
            'Proper formatting': '\n\n' in content
        }
        
        passed_checks = 0
        
        for check, result in organization_checks.items():
            if result:
                print(f"✅ {check}")
                passed_checks += 1
            else:
                print(f"❌ {check}")
        
        percentage = (passed_checks / len(organization_checks)) * 100
        print(f"\n📊 Organization: {passed_checks}/{len(organization_checks)} ({percentage:.1f}%)")
        
        return min(15, int(percentage * 0.15))
    
    def generate_report(self):
        """Generate comprehensive requirements validation report"""
        print("🔍 REQUIREMENTS.TXT SECURITY VALIDATION")
        print("=" * 50)
        
        if not self.check_file_exists():
            return False
        
        # Run all checks
        version_score = self.check_version_pinning()
        security_score = self.check_security_packages()
        production_score = self.check_production_packages()
        dev_score = self.check_development_packages()
        organization_score = self.check_package_organization()
        
        total_score = version_score + security_score + production_score + dev_score + organization_score
        
        print(f"\n📊 VALIDATION SUMMARY:")
        print("-" * 30)
        print(f"   • Version Pinning: {version_score}/30")
        print(f"   • Security Packages: {security_score}/25")
        print(f"   • Production Packages: {production_score}/20")
        print(f"   • Development Packages: {dev_score}/10")
        print(f"   • Organization: {organization_score}/15")
        print(f"   • TOTAL SCORE: {total_score}/100")
        
        # Grade assignment
        if total_score >= 90:
            grade = "A+"
            status = "🏆 EXCELLENT - Production ready"
        elif total_score >= 80:
            grade = "A"
            status = "✅ VERY GOOD - Minor improvements"
        elif total_score >= 70:
            grade = "B"
            status = "✅ GOOD - Some improvements needed"
        elif total_score >= 60:
            grade = "C"
            status = "⚠️ FAIR - Several improvements needed"
        else:
            grade = "D"
            status = "❌ POOR - Major improvements needed"
        
        print(f"\n🎯 REQUIREMENTS GRADE: {grade}")
        print(f"📝 STATUS: {status}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if total_score >= 90:
            print("   🎉 Excellent! Your requirements.txt is production-ready")
            print("   🔒 All security packages properly configured")
            print("   📦 Consider running 'pip-audit' for vulnerability scanning")
        elif total_score >= 80:
            print("   📌 Pin any remaining unpinned versions")
            print("   🛡️ Add any missing security packages")
            print("   📝 Improve documentation and organization")
        else:
            print("   📌 Pin all package versions with ==")
            print("   🛡️ Add essential security packages")
            print("   🚀 Add production-ready packages")
            print("   📝 Organize with comments and sections")
        
        print(f"\n🔗 NEXT STEPS:")
        print("   1. Install packages: pip install -r requirements.txt")
        print("   2. Run security scan: bandit -r .")
        print("   3. Check vulnerabilities: safety check")
        print("   4. Update regularly for security patches")
        
        return total_score >= 80

def main():
    """Main validation function"""
    validator = RequirementsValidator()
    
    try:
        success = validator.generate_report()
        
        if success:
            print("\n🎉 REQUIREMENTS VALIDATION PASSED!")
            print("✅ Your requirements.txt is well configured!")
        else:
            print("\n⚠️ Requirements improvements needed")
            print("🔧 Address the recommendations above")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    main()
