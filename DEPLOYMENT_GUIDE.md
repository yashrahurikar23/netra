# 🚀 Netra Deployment Guide - Cheapest Strategies

## Overview

This guide covers the most cost-effective ways to deploy the Netra space flight simulation and RAG platform. We'll explore free and low-cost options, from completely free platforms to budget-friendly cloud solutions.

## 📊 Cost Comparison Summary

| Platform | Cost | Pros | Cons | Best For |
|----------|------|------|------|----------|
| **Streamlit Community Cloud** | **FREE** | Zero cost, easy setup, GitHub integration | Limited resources, public repos only | Demos, portfolios, open-source |
| **Hugging Face Spaces** | **FREE** | Free tier, good for ML apps | Limited compute, 16GB storage | AI/ML demos, prototypes |
| **Railway** | **$5-20/month** | Simple deployment, good free tier | Limited free hours | Small to medium apps |
| **Render** | **$7-25/month** | Good performance, easy scaling | No permanent free tier | Production apps |
| **DigitalOcean Droplet** | **$4-12/month** | Full control, predictable pricing | Requires server management | Self-managed deployments |
| **Google Cloud Run** | **Pay-per-use** | Serverless, scales to zero | Complex pricing, cold starts | Variable traffic apps |

---

## 🆓 FREE Deployment Options

### 1. **Streamlit Community Cloud** ⭐ RECOMMENDED FOR FREE

**Cost:** Completely FREE
**Requirements:** Public GitHub repository

**Setup Steps:**
1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy Netra app"
   git push origin main
   ```

2. **Create deployment files:**
   ```bash
   # Create requirements.txt (already exists)
   # Create packages.txt for system dependencies
   echo "libgl1-mesa-glx" > packages.txt
   
   # Create secrets.toml template
   mkdir .streamlit
   echo '[general]
   email = "your-email@example.com"
   
   [server]
   headless = true
   port = $PORT
   
   [openai]
   api_key = "your-openai-api-key"' > .streamlit/secrets.toml
   ```

3. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `src/ui/main_app.py`
   - Add secrets in the dashboard

**Limitations:**
- Must be a public repository
- Limited to 1GB RAM, 1 CPU core
- 1GB storage space
- Apps sleep after 7 days of inactivity

**Optimization for Free Tier:**
```python
# Add to your main_app.py to reduce memory usage
import streamlit as st

@st.cache_data
def load_large_data():
    """Cache expensive operations"""
    pass

@st.cache_resource
def initialize_models():
    """Cache model initialization"""
    pass
```

### 2. **Hugging Face Spaces**

**Cost:** FREE (with limitations)
**Requirements:** Hugging Face account

**Setup:**
1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose "Streamlit" as the SDK
3. Upload your code files
4. Create `requirements.txt` and `app.py`

**Example app.py for HF Spaces:**
```python
#!/usr/bin/env python3
import subprocess
import sys
import os

# Install requirements
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Set environment
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Import and run your app
sys.path.append("src")
from ui.main_app import main

if __name__ == "__main__":
    main()
```

**Limitations:**
- 16GB storage
- Limited CPU/memory
- Public only (unless you have a paid plan)

---

## 💰 LOW-COST PAID OPTIONS

### 3. **Railway** - Best Value for Small Apps

**Cost:** $5-20/month (500 hours free monthly)

**Setup:**
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Create railway.toml:**
   ```toml
   [build]
   builder = "nixpacks"
   
   [deploy]
   startCommand = "streamlit run src/ui/main_app.py --server.port=$PORT --server.address=0.0.0.0"
   ```

**Benefits:**
- Simple deployment process
- Good performance
- Environment variable management
- Database support

### 4. **Render** - Production Ready

**Cost:** $7-25/month

**Setup:**
1. Connect your GitHub repository
2. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: netra-app
       env: python
       plan: starter
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run src/ui/main_app.py --server.port=$PORT --server.address=0.0.0.0
       envVars:
         - key: PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION
           value: python
   ```

**Benefits:**
- Automatic deployments
- SSL certificates
- Good performance
- Monitoring included

### 5. **DigitalOcean Droplet** - Self Managed

**Cost:** $4-12/month

**Setup Script:**
```bash
#!/bin/bash
# Ubuntu 22.04 setup script

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv nginx git

# Clone your repository
git clone <your-repo-url> /home/netra
cd /home/netra

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/netra.service > /dev/null <<EOF
[Unit]
Description=Netra Streamlit App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/netra
Environment=PATH=/home/netra/venv/bin
Environment=PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ExecStart=/home/netra/venv/bin/streamlit run src/ui/main_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl enable netra
sudo systemctl start netra

# Configure nginx
sudo tee /etc/nginx/sites-available/netra > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/netra /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ⚡ SERVERLESS OPTIONS

### 6. **Google Cloud Run**

**Cost:** Pay per use (very cheap for low traffic)

**Setup:**
1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
   
   EXPOSE 8080
   
   CMD ["streamlit", "run", "src/ui/main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
   ```

2. **Deploy:**
   ```bash
   gcloud run deploy netra-app --source . --platform managed --region us-central1 --allow-unauthenticated
   ```

**Benefits:**
- Scales to zero (no cost when not used)
- Automatic scaling
- Pay only for actual usage

---

## 🔧 OPTIMIZATION STRATEGIES

### Memory Optimization

```python
# In your main_app.py
import streamlit as st
import gc

# Use caching extensively
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_heavy_data():
    pass

@st.cache_resource
def initialize_simulation():
    pass

# Clear memory periodically
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    gc.collect()
```

### Environment Variables Setup

Create `.env` file:
```bash
# Required for protobuf compatibility
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# OpenAI API (required for RAG)
OPENAI_API_KEY=your_api_key_here

# Optional: Reduce memory usage
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
STREAMLIT_SERVER_MAX_MESSAGE_SIZE=50
```

### Lightweight Requirements

Create `requirements-lite.txt` for deployment:
```txt
streamlit>=1.31.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
protobuf==3.20.3

# Only include if RAG is needed
# llama-index>=0.10.0
# chromadb>=0.4.0
# openai>=1.12.0
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Test app locally with production settings
- [ ] Optimize memory usage with caching
- [ ] Set up environment variables
- [ ] Create deployment configuration files
- [ ] Test with limited resources

### Free Tier Deployment
- [ ] Make repository public (for Streamlit Cloud)
- [ ] Add secrets in platform dashboard
- [ ] Test with sample data
- [ ] Monitor resource usage

### Paid Deployment
- [ ] Set up domain name (optional)
- [ ] Configure SSL certificates
- [ ] Set up monitoring and alerts
- [ ] Plan for scaling

---

## 💡 RECOMMENDATIONS BY USE CASE

### **For Demos/Portfolios:** 
**Streamlit Community Cloud** (FREE)
- Perfect for showcasing your work
- Easy setup and maintenance
- Good enough performance for demonstrations

### **For Development/Testing:** 
**Hugging Face Spaces** (FREE) or **Railway** ($5/month)
- Good for iterative development
- Easy to share with team members

### **For Production Apps:** 
**Render** ($7/month) or **DigitalOcean** ($12/month)
- Reliable performance
- Better support and monitoring
- Suitable for real users

### **For Variable Traffic:** 
**Google Cloud Run** (Pay-per-use)
- Cost-effective for apps with unpredictable usage
- Automatic scaling

---

## 🔍 MONITORING AND MAINTENANCE

### Basic Monitoring
```python
# Add to your app for basic analytics
import streamlit as st
from datetime import datetime

if 'page_views' not in st.session_state:
    st.session_state.page_views = 0

st.session_state.page_views += 1

# Log usage (for debugging)
with open('usage.log', 'a') as f:
    f.write(f"{datetime.now()}: Page view #{st.session_state.page_views}\n")
```

### Health Check Endpoint
```python
# Add to your app
if st.sidebar.button("Health Check"):
    try:
        # Test core functionality
        from physics.simulation import SpaceFlightSimulation
        sim = SpaceFlightSimulation()
        st.success("✅ App is healthy")
    except Exception as e:
        st.error(f"❌ Health check failed: {e}")
```

---

## 🎯 FINAL RECOMMENDATION

**For the Netra app specifically:**

1. **Start with Streamlit Community Cloud (FREE)** if you can make the repo public
2. **Upgrade to Railway ($5/month)** when you need private repos or more resources
3. **Move to Render ($7/month)** for production use with real users

The physics simulation and RAG components work well on all these platforms with proper optimization. The key is to start simple and scale as needed.

---

## 📞 TROUBLESHOOTING

### Common Issues:
- **Memory errors:** Use more caching, reduce data loading
- **Protobuf errors:** Set `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`
- **Slow loading:** Optimize imports, use lazy loading
- **OpenAI API costs:** Cache responses, limit query frequency

### Platform-Specific Tips:
- **Streamlit Cloud:** Keep under 1GB RAM usage
- **Railway:** Use build cache to speed up deployments
- **Render:** Enable automatic deploys for continuous deployment
- **Cloud Run:** Optimize cold start times with lighter images

This deployment guide gives you multiple options ranging from completely free to low-cost production deployments, all optimized for the Netra platform's specific requirements.
