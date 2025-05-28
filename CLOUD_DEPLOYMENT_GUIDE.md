# ☁️ Cloud Deployment Guide

Deploy your Instagram automation system to the cloud with Docker and ngrok's free domain for global access.

## 🎯 Deployment Overview

### **What You'll Get:**
- 🌍 **Global Access** - Access your automation from anywhere
- 🆓 **Free Ngrok Domain** - No cost for external access
- 🐳 **Dockerized Services** - Scalable and portable
- 📊 **Built-in Monitoring** - Health checks and uptime monitoring
- 🔒 **Secure Setup** - Authentication and SSL via ngrok

### **Architecture:**
```text
Internet → Ngrok (Free Domain) → Cloud Server → Docker Containers
                                                      ├── n8n (Workflows)
                                                      ├── Mock API (MCP Tools)
                                                      ├── Redis (Caching)
                                                      └── Monitoring
```

## 🚀 Quick Deployment

### **Step 1: Get Ngrok Free Account**

1. Go to [ngrok.com](https://ngrok.com) and sign up (FREE)
2. Get your authtoken from [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Copy the token for configuration

### **Step 2: Configure Environment**

```bash
# Copy cloud environment template
cp .env.cloud.example .env.cloud

# Edit with your settings
nano .env.cloud
```

**Required Configuration:**
```bash
# Ngrok (FREE)
NGROK_AUTHTOKEN=your_free_ngrok_token

# n8n Authentication
N8N_BASIC_AUTH_USER=your_username
N8N_BASIC_AUTH_PASSWORD=your_secure_password

# Optional: Custom subdomains (ngrok free tier)
NGROK_N8N_SUBDOMAIN=my-instagram-bot
NGROK_API_SUBDOMAIN=my-api-server
```

### **Step 3: Deploy to Cloud**

```bash
# One-command deployment
python deploy-cloud.py
```

**Or manual deployment:**
```bash
# Build and deploy
docker-compose -f docker-compose.cloud.yml --env-file .env.cloud up -d
```

## 🌐 Cloud Provider Setup

### **AWS EC2 (Recommended)**

#### **Launch Instance:**
```bash
# Instance type: t3.micro (Free tier eligible)
# OS: Ubuntu 22.04 LTS
# Storage: 20GB GP3
# Security Group: Allow ports 22, 80, 443, 5678, 8000
```

#### **Setup Commands:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repository
git clone https://github.com/Gmpho/autmation-tasks.git
cd autmation-tasks

# Configure and deploy
cp .env.cloud.example .env.cloud
nano .env.cloud  # Add your configuration
python deploy-cloud.py
```

### **Google Cloud Platform (GCP)**

#### **Compute Engine:**
```bash
# Create VM instance
gcloud compute instances create instagram-automation \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-micro \
    --boot-disk-size=20GB \
    --tags=http-server,https-server

# SSH and setup (same as AWS commands above)
```

### **DigitalOcean Droplet**

#### **Create Droplet:**
- **Image**: Ubuntu 22.04 LTS
- **Plan**: Basic ($4/month)
- **Size**: 1GB RAM, 1 vCPU, 25GB SSD
- **Datacenter**: Choose closest to your location

#### **Setup:** Same commands as AWS

### **Azure Container Instances**

#### **Deploy Container:**
```bash
# Create resource group
az group create --name instagram-automation --location eastus

# Deploy container
az container create \
    --resource-group instagram-automation \
    --name instagram-bot \
    --image your-registry/instagram-automation:latest \
    --ports 5678 8000 \
    --environment-variables NGROK_AUTHTOKEN=your_token
```

## 🔧 Configuration Options

### **Environment Variables**

#### **Required:**
```bash
NGROK_AUTHTOKEN=your_ngrok_token
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure_password
```

#### **Optional:**
```bash
# Custom domains (ngrok free tier)
NGROK_N8N_SUBDOMAIN=my-automation
NGROK_API_SUBDOMAIN=my-api

# AI APIs (when ready for production)
CLAUDE_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_token

# Performance tuning
N8N_LOG_LEVEL=info
FLASK_ENV=production
MOCK_MODE=true
```

### **Resource Requirements**

| Component | CPU | RAM | Storage | Cost/Month |
|-----------|-----|-----|---------|------------|
| **Minimum** | 1 vCPU | 1GB | 20GB | $4-6 |
| **Recommended** | 2 vCPU | 2GB | 40GB | $10-15 |
| **High Performance** | 4 vCPU | 4GB | 80GB | $20-30 |

## 📊 Monitoring & Management

### **Access Points:**

#### **External (via ngrok):**
- **n8n Dashboard**: `https://your-subdomain.ngrok-free.app`
- **API Server**: `https://your-api-subdomain.ngrok-free.app`
- **Monitoring**: `https://your-subdomain.ngrok-free.app:3001`

#### **Local (on server):**
- **n8n**: `http://localhost:5678`
- **Mock API**: `http://localhost:8000`
- **Ngrok Dashboard**: `http://localhost:4040`

### **Management Commands:**

```bash
# View service status
docker-compose -f docker-compose.cloud.yml ps

# View logs
docker-compose -f docker-compose.cloud.yml logs -f

# Restart services
docker-compose -f docker-compose.cloud.yml restart

# Update deployment
git pull
docker-compose -f docker-compose.cloud.yml up -d --build

# Stop services
docker-compose -f docker-compose.cloud.yml down

# Backup data
docker run --rm -v instagram_automation_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup.tar.gz -C /data .
```

## 💰 Cost Breakdown

### **Free Tier Options:**
- **Ngrok**: FREE (with limits)
- **AWS EC2**: t3.micro free for 12 months
- **GCP**: $300 credit for new accounts
- **Oracle Cloud**: Always free tier available

### **Estimated Monthly Costs:**

| Provider | Instance | Cost | Ngrok | Total |
|----------|----------|------|-------|-------|
| **AWS EC2** | t3.micro | $8.50 | FREE | $8.50 |
| **DigitalOcean** | Basic | $4.00 | FREE | $4.00 |
| **GCP** | e2-micro | $6.00 | FREE | $6.00 |
| **Azure** | B1s | $7.50 | FREE | $7.50 |

### **Additional Costs (Optional):**
- **AI APIs**: $5-20/month (when using real APIs)
- **Domain**: $10-15/year (if you want custom domain)
- **SSL Certificate**: FREE (via ngrok or Let's Encrypt)

## 🛡️ Security Best Practices

### **Authentication:**
- ✅ Enable n8n basic auth (required)
- ✅ Use strong passwords
- ✅ Enable ngrok authentication
- ✅ Restrict IP access if needed

### **Network Security:**
- ✅ Use HTTPS via ngrok
- ✅ Configure firewall rules
- ✅ Regular security updates
- ✅ Monitor access logs

### **Data Protection:**
- ✅ Regular backups
- ✅ Encrypt sensitive data
- ✅ Use environment variables
- ✅ Rotate API keys regularly

## 🚀 Scaling Options

### **Horizontal Scaling:**
- Multiple instances behind load balancer
- Database clustering
- Redis cluster for caching

### **Vertical Scaling:**
- Increase CPU/RAM as needed
- Add storage for data growth
- Optimize container resources

## 🆘 Troubleshooting

### **Common Issues:**

#### **Ngrok Connection Failed:**
```bash
# Check authtoken
docker-compose -f docker-compose.cloud.yml logs ngrok

# Verify token in .env.cloud
grep NGROK_AUTHTOKEN .env.cloud
```

#### **Services Not Starting:**
```bash
# Check logs
docker-compose -f docker-compose.cloud.yml logs

# Check system resources
docker system df
free -h
```

#### **Can't Access Externally:**
```bash
# Check ngrok tunnels
curl http://localhost:4040/api/tunnels

# Verify firewall
sudo ufw status
```

## 🎉 Success Checklist

- ✅ Cloud server running
- ✅ Docker containers healthy
- ✅ Ngrok tunnels active
- ✅ External access working
- ✅ Authentication configured
- ✅ Monitoring enabled
- ✅ Backups configured

**Your Instagram automation is now running in the cloud with global access!** 🌍

---

💡 **Pro Tip**: Start with the free tier and scale up as your automation grows. The mock APIs let you develop and test everything without any API costs!
