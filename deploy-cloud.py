#!/usr/bin/env python3
"""
Cloud Deployment Script for Instagram Automation
Supports AWS, GCP, Azure, DigitalOcean, and other cloud providers
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

class CloudDeployer:
    def __init__(self):
        self.project_name = "instagram-automation"
        self.load_environment()
        
    def load_environment(self):
        """Load cloud environment variables"""
        env_file = Path('.env.cloud')
        if env_file.exists():
            load_dotenv(env_file)
            print("✅ Loaded cloud environment configuration")
        else:
            print("❌ .env.cloud file not found!")
            print("💡 Copy .env.cloud.example to .env.cloud and configure it")
            sys.exit(1)
    
    def check_prerequisites(self):
        """Check if all prerequisites are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Docker
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker: {result.stdout.strip()}")
            else:
                print("❌ Docker not found")
                return False
        except FileNotFoundError:
            print("❌ Docker not installed")
            return False
        
        # Check Docker Compose
        try:
            result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker Compose: {result.stdout.strip()}")
            else:
                print("❌ Docker Compose not found")
                return False
        except FileNotFoundError:
            print("❌ Docker Compose not installed")
            return False
        
        # Check required environment variables
        required_vars = [
            'NGROK_AUTHTOKEN',
            'N8N_BASIC_AUTH_USER',
            'N8N_BASIC_AUTH_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("💡 Configure these in your .env.cloud file")
            return False
        
        print("✅ All prerequisites met")
        return True
    
    def build_images(self):
        """Build Docker images"""
        print("🏗️ Building Docker images...")
        
        try:
            # Build mock API image
            subprocess.run([
                'docker', 'build', 
                '-f', 'Dockerfile.mock-api',
                '-t', f'{self.project_name}-api:latest',
                '.'
            ], check=True)
            print("✅ Mock API image built successfully")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build images: {e}")
            return False
    
    def deploy_services(self):
        """Deploy services using Docker Compose"""
        print("🚀 Deploying services...")
        
        try:
            # Stop any existing services
            subprocess.run([
                'docker-compose', '-f', 'docker-compose.cloud.yml',
                'down'
            ], capture_output=True)
            
            # Start services
            subprocess.run([
                'docker-compose', '-f', 'docker-compose.cloud.yml',
                '--env-file', '.env.cloud',
                'up', '-d'
            ], check=True)
            
            print("✅ Services deployed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to deploy services: {e}")
            return False
    
    def wait_for_services(self):
        """Wait for services to be healthy"""
        print("⏳ Waiting for services to start...")
        
        services = {
            'Mock API': 'http://localhost:8000/health',
            'n8n': 'http://localhost:5678/healthz',
            'Ngrok Dashboard': 'http://localhost:4040/api/tunnels'
        }
        
        max_wait = 120  # 2 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            all_healthy = True
            
            for service_name, url in services.items():
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        print(f"✅ {service_name} is healthy")
                    else:
                        print(f"⏳ {service_name} starting...")
                        all_healthy = False
                except requests.exceptions.RequestException:
                    print(f"⏳ {service_name} starting...")
                    all_healthy = False
            
            if all_healthy:
                print("🎉 All services are healthy!")
                return True
            
            time.sleep(10)
        
        print("⚠️ Some services may still be starting")
        return True
    
    def get_ngrok_urls(self):
        """Get ngrok tunnel URLs"""
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=10)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                urls = {}
                
                for tunnel in tunnels:
                    name = tunnel['name']
                    public_url = tunnel['public_url']
                    urls[name] = public_url
                
                return urls
            else:
                print("⚠️ Could not retrieve ngrok URLs")
                return {}
        except Exception as e:
            print(f"⚠️ Error getting ngrok URLs: {e}")
            return {}
    
    def display_deployment_info(self):
        """Display deployment information"""
        print("\n" + "="*60)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("="*60)
        
        # Get ngrok URLs
        ngrok_urls = self.get_ngrok_urls()
        
        print("\n🌐 Access Points:")
        print("-" * 30)
        
        # Local access
        print("📍 Local Access:")
        print(f"   • n8n Dashboard: http://localhost:5678")
        print(f"   • Mock API: http://localhost:8000")
        print(f"   • Ngrok Dashboard: http://localhost:4040")
        print(f"   • Monitoring: http://localhost:3001")
        
        # External access via ngrok
        if ngrok_urls:
            print("\n🌍 External Access (via ngrok):")
            for name, url in ngrok_urls.items():
                print(f"   • {name.title()}: {url}")
        
        print("\n🔐 Authentication:")
        print(f"   • Username: {os.getenv('N8N_BASIC_AUTH_USER')}")
        print(f"   • Password: {os.getenv('N8N_BASIC_AUTH_PASSWORD')}")
        
        print("\n💰 Cost Information:")
        print("   • Ngrok: FREE (with limits)")
        print("   • Mock APIs: $0.00")
        print("   • Cloud hosting: Varies by provider")
        
        print("\n📋 Next Steps:")
        print("   1. Access n8n via the external URL")
        print("   2. Create your automation workflows")
        print("   3. Test with mock APIs (free)")
        print("   4. Add real API keys when ready")
        print("   5. Monitor via the dashboard")
        
        print("\n🛠️ Management Commands:")
        print("   • View logs: docker-compose -f docker-compose.cloud.yml logs")
        print("   • Stop services: docker-compose -f docker-compose.cloud.yml down")
        print("   • Restart: docker-compose -f docker-compose.cloud.yml restart")
        
        print("="*60)
    
    def deploy(self):
        """Main deployment function"""
        print("🚀 Instagram Automation - Cloud Deployment")
        print("="*50)
        
        if not self.check_prerequisites():
            return False
        
        if not self.build_images():
            return False
        
        if not self.deploy_services():
            return False
        
        if not self.wait_for_services():
            return False
        
        self.display_deployment_info()
        return True

def main():
    """Main function"""
    deployer = CloudDeployer()
    
    try:
        success = deployer.deploy()
        if success:
            print("\n🎉 Deployment completed successfully!")
            print("💡 Your Instagram automation is now running in the cloud!")
        else:
            print("\n❌ Deployment failed!")
            print("💡 Check the error messages above and try again")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
