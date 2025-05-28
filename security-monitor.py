#!/usr/bin/env python3
"""
Security Monitoring and Alerting System
Real-time security monitoring for production deployment
"""

import os
import time
import json
import logging
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class SecurityMonitor:
    """Real-time security monitoring system"""
    
    def __init__(self):
        self.setup_logging()
        self.alerts = []
        self.last_check = datetime.now()
        
    def setup_logging(self):
        """Setup security monitoring logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SECURITY - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/app/logs/security-monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SecurityMonitor')
    
    def check_container_security(self):
        """Monitor container security status"""
        try:
            # Check if running as non-root
            result = subprocess.run(['whoami'], capture_output=True, text=True)
            if result.returncode == 0:
                user = result.stdout.strip()
                if user == 'appuser':
                    self.logger.info("✅ Container running as non-root user")
                else:
                    self.alert("❌ Container running as root user", "HIGH")
            
            # Check file permissions
            app_files = ['/app/mock_api_server.py', '/app/mcp_integration.py']
            for file_path in app_files:
                if os.path.exists(file_path):
                    stat = os.stat(file_path)
                    permissions = oct(stat.st_mode)[-3:]
                    if permissions == '644':
                        self.logger.info(f"✅ Secure permissions for {file_path}")
                    else:
                        self.alert(f"⚠️ Insecure permissions for {file_path}: {permissions}", "MEDIUM")
            
            return True
        except Exception as e:
            self.alert(f"Error checking container security: {e}", "HIGH")
            return False
    
    def check_network_security(self):
        """Monitor network security"""
        try:
            # Check if application is responding
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                self.logger.info("✅ Application health check passed")
                
                # Check security headers
                required_headers = [
                    'X-Content-Type-Options',
                    'X-Frame-Options',
                    'X-XSS-Protection'
                ]
                
                missing_headers = []
                for header in required_headers:
                    if header not in response.headers:
                        missing_headers.append(header)
                
                if missing_headers:
                    self.alert(f"⚠️ Missing security headers: {missing_headers}", "MEDIUM")
                else:
                    self.logger.info("✅ All security headers present")
            else:
                self.alert(f"❌ Application health check failed: {response.status_code}", "HIGH")
            
            return True
        except requests.exceptions.RequestException as e:
            self.alert(f"Network security check failed: {e}", "HIGH")
            return False
    
    def check_log_anomalies(self):
        """Check for security anomalies in logs"""
        try:
            log_file = Path('/app/logs/security.log')
            if not log_file.exists():
                return True
            
            # Read recent log entries
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            # Check for suspicious patterns
            suspicious_patterns = [
                'injection attempt',
                'malicious input',
                'unauthorized access',
                'failed authentication',
                'rate limit exceeded'
            ]
            
            recent_lines = lines[-100:]  # Check last 100 lines
            alerts_found = []
            
            for line in recent_lines:
                for pattern in suspicious_patterns:
                    if pattern.lower() in line.lower():
                        alerts_found.append(line.strip())
            
            if alerts_found:
                self.alert(f"⚠️ Suspicious activity detected: {len(alerts_found)} incidents", "MEDIUM")
                for alert in alerts_found[-5:]:  # Show last 5
                    self.logger.warning(f"Suspicious: {alert}")
            else:
                self.logger.info("✅ No suspicious activity in logs")
            
            return True
        except Exception as e:
            self.alert(f"Error checking logs: {e}", "LOW")
            return False
    
    def check_resource_usage(self):
        """Monitor resource usage for DoS attacks"""
        try:
            # Check memory usage
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            mem_total = None
            mem_available = None
            
            for line in meminfo.split('\n'):
                if line.startswith('MemTotal:'):
                    mem_total = int(line.split()[1])
                elif line.startswith('MemAvailable:'):
                    mem_available = int(line.split()[1])
            
            if mem_total and mem_available:
                usage_percent = ((mem_total - mem_available) / mem_total) * 100
                
                if usage_percent > 90:
                    self.alert(f"❌ High memory usage: {usage_percent:.1f}%", "HIGH")
                elif usage_percent > 80:
                    self.alert(f"⚠️ Elevated memory usage: {usage_percent:.1f}%", "MEDIUM")
                else:
                    self.logger.info(f"✅ Memory usage normal: {usage_percent:.1f}%")
            
            return True
        except Exception as e:
            self.alert(f"Error checking resource usage: {e}", "LOW")
            return False
    
    def alert(self, message, severity="INFO"):
        """Generate security alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity
        }
        
        self.alerts.append(alert)
        
        # Log based on severity
        if severity == "HIGH":
            self.logger.error(message)
        elif severity == "MEDIUM":
            self.logger.warning(message)
        else:
            self.logger.info(message)
        
        # Send webhook notification for high severity
        if severity == "HIGH":
            self.send_webhook_alert(alert)
    
    def send_webhook_alert(self, alert):
        """Send webhook notification for critical alerts"""
        webhook_url = os.getenv('SECURITY_WEBHOOK_URL')
        if not webhook_url:
            return
        
        try:
            payload = {
                'text': f"🚨 SECURITY ALERT: {alert['message']}",
                'severity': alert['severity'],
                'timestamp': alert['timestamp'],
                'service': 'Instagram Automation'
            }
            
            requests.post(webhook_url, json=payload, timeout=10)
            self.logger.info("Security alert sent via webhook")
        except Exception as e:
            self.logger.error(f"Failed to send webhook alert: {e}")
    
    def generate_security_report(self):
        """Generate security monitoring report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'monitoring_duration': str(datetime.now() - self.last_check),
            'total_alerts': len(self.alerts),
            'alerts_by_severity': {
                'HIGH': len([a for a in self.alerts if a['severity'] == 'HIGH']),
                'MEDIUM': len([a for a in self.alerts if a['severity'] == 'MEDIUM']),
                'LOW': len([a for a in self.alerts if a['severity'] == 'LOW'])
            },
            'recent_alerts': self.alerts[-10:] if self.alerts else []
        }
        
        return report
    
    def run_monitoring_cycle(self):
        """Run complete monitoring cycle"""
        self.logger.info("🔍 Starting security monitoring cycle")
        
        checks = [
            ("Container Security", self.check_container_security),
            ("Network Security", self.check_network_security),
            ("Log Anomalies", self.check_log_anomalies),
            ("Resource Usage", self.check_resource_usage)
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                self.alert(f"Monitoring check failed: {check_name} - {e}", "HIGH")
                results[check_name] = False
        
        # Generate report
        report = self.generate_security_report()
        
        # Log summary
        passed_checks = sum(1 for result in results.values() if result)
        total_checks = len(results)
        
        self.logger.info(f"✅ Monitoring cycle complete: {passed_checks}/{total_checks} checks passed")
        
        if passed_checks == total_checks:
            self.logger.info("🛡️ All security checks passed")
        else:
            self.alert(f"⚠️ {total_checks - passed_checks} security checks failed", "MEDIUM")
        
        return report

def main():
    """Main monitoring function"""
    print("🛡️ Security Monitoring System for Instagram Automation")
    print("=" * 60)
    
    monitor = SecurityMonitor()
    
    try:
        # Run single monitoring cycle
        report = monitor.run_monitoring_cycle()
        
        print("\n📊 SECURITY MONITORING REPORT:")
        print("-" * 40)
        print(f"Monitoring Duration: {report['monitoring_duration']}")
        print(f"Total Alerts: {report['total_alerts']}")
        print(f"High Severity: {report['alerts_by_severity']['HIGH']}")
        print(f"Medium Severity: {report['alerts_by_severity']['MEDIUM']}")
        print(f"Low Severity: {report['alerts_by_severity']['LOW']}")
        
        if report['recent_alerts']:
            print("\n🚨 Recent Alerts:")
            for alert in report['recent_alerts'][-5:]:
                print(f"   • {alert['severity']}: {alert['message']}")
        else:
            print("\n✅ No security alerts")
        
        print("\n🎯 Security Status: MONITORING ACTIVE")
        
    except KeyboardInterrupt:
        print("\n⚠️ Monitoring interrupted")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")

if __name__ == "__main__":
    main()
