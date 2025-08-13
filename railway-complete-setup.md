# Complete Railway Deployment Guide for GoldBrella

This guide will deploy your **complete solution** on Railway: Backend + Frontend + Database.

## 🎯 **What We're Deploying**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React/Vue)   │◄──►│   (Django API)  │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis         │
                       │   (Memorystore) │
                       └─────────────────┘
```

## 🚀 **Step 1: Railway Project Setup**

### 1.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project: "goldbrella"

### 1.2 Project Structure
Your Railway project will have these services:
- `goldbrella-backend` (Django API)
- `goldbrella-frontend` (React/Vue app)
- `goldbrella-db` (PostgreSQL)
- `goldbrella-redis` (Redis)

## 🐍 **Step 2: Deploy Backend (Django)**

### 2.1 Add Backend Service
1. **Add Service** → **GitHub Repo**
2. Select your `goldbrella-backend` repository
3. Railway will auto-detect your Dockerfile
4. Service name: `goldbrella-backend`

### 2.2 Configure Backend
Railway will automatically:
- ✅ Build from Dockerfile
- ✅ Deploy to container
- ✅ Provide public URL
- ✅ Handle scaling

### 2.3 Backend Environment Variables
Add these in Railway dashboard:

```bash
# Django Core
DJANGO_SETTINGS_MODULE=goldbrella.settings
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.railway.app

# JWT Settings
ACCESS_TOKEN_LIFETIME=300
REFRESH_TOKEN_LIFETIME=86400
ROTATE_REFRESH_TOKENS=true

# Site URL (will be your Railway backend URL)
SITE_URL=https://your-backend-name.railway.app

# Email (configure as needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=true

# Stripe (configure as needed)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## 🗄️ **Step 3: Add Databases**

### 3.1 Add PostgreSQL
1. **Add Service** → **Database** → **PostgreSQL**
2. Service name: `goldbrella-db`
3. Railway automatically provides `DATABASE_URL`

### 3.2 Add Redis
1. **Add Service** → **Database** → **Redis**
2. Service name: `goldbrella-redis`
3. Railway automatically provides `REDIS_URL`

### 3.3 Database Environment Variables
Railway automatically sets these (don't add manually):
```bash
DATABASE_URL=postgresql://... (auto-set)
REDIS_URL=redis://... (auto-set)
```

## 🎨 **Step 4: Deploy Frontend**

### 4.1 Option A: Railway Static Hosting (Recommended)

#### Create Frontend Service
1. **Add Service** → **Static Site**
2. Connect your frontend repository
3. Configure build settings:

```bash
# Build Command
npm run build

# Publish Directory
dist  # (or 'build' for Create React App)

# Install Command
npm install
```

#### Frontend Environment Variables
Add these for your frontend:

```bash
# API Base URL (your backend Railway URL)
VITE_API_BASE_URL=https://your-backend-name.railway.app
# or
REACT_APP_API_BASE_URL=https://your-backend-name.railway.app

# Other frontend config
VITE_APP_NAME=GoldBrella
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 4.2 Option B: Deploy Frontend to Vercel (Alternative)

If you prefer Vercel for frontend:

1. Go to [vercel.com](https://vercel.com)
2. Import your frontend repository
3. Set environment variables
4. Deploy

## 🔄 **Step 5: Database Migration**

### 5.1 Run Django Migrations
Railway provides a CLI for this:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Connect to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

### 5.2 Alternative: Railway Dashboard
1. Go to your backend service
2. Click "Deployments"
3. Create new deployment with custom command:
   ```bash
   python manage.py migrate
   ```

## 🌐 **Step 6: Custom Domain Setup**

### 6.1 Add Custom Domain
1. Go to your service settings
2. **Custom Domains** → **Add Domain**
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Follow DNS setup instructions

### 6.2 DNS Configuration
Add these records to your domain provider:

```bash
# Backend API
Type: CNAME
Name: api
Value: your-backend-name.railway.app

# Frontend
Type: CNAME
Name: www
Value: your-frontend-name.railway.app
```

## 🔧 **Step 7: Environment Configuration**

### 7.1 Update Django Settings
Your Django app needs to work with Railway's environment:

```python
# In your settings.py, ensure these work with Railway:
import os
from urllib.parse import urlparse

# Database (Railway provides DATABASE_URL)
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }

# Redis (Railway provides REDIS_URL)
if 'REDIS_URL' in os.environ:
    CELERY_BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
```

### 7.2 Update Frontend Configuration
Ensure your frontend can connect to the backend:

```javascript
// In your frontend config
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API calls
const response = await fetch(`${API_BASE_URL}/api/endpoint/`);
```

## 🧪 **Step 8: Testing**

### 8.1 Test Backend
```bash
# Test your API
curl https://your-backend-name.railway.app/api/health/
curl https://your-backend-name.railway.app/docs/
```

### 8.2 Test Frontend
1. Open your frontend URL
2. Test API connections
3. Verify all features work

### 8.3 Test Database
```bash
# Check database connection
railway run python manage.py dbshell

# List tables
\dt
```

## 📊 **Step 9: Monitoring & Scaling**

### 9.1 Railway Dashboard
- **Metrics**: CPU, memory, requests
- **Logs**: Real-time application logs
- **Deployments**: Deployment history

### 9.2 Scaling Options
- **Auto-scaling**: Based on traffic
- **Manual scaling**: Set instance count
- **Resource limits**: CPU/memory allocation

## 💰 **Cost Breakdown**

### Free Tier (Railway)
- **$5/month credit** included
- **Backend hosting**: ~$1-2/month
- **PostgreSQL**: ~$2-3/month
- **Redis**: ~$1-2/month
- **Frontend hosting**: ~$0-1/month
- **Total**: Usually under $5/month (FREE!)

### Paid Plans
- **Pro**: $20/month (more resources)
- **Team**: $20/month per user
- **Enterprise**: Custom pricing

## 🎯 **Advantages of Railway**

✅ **Complete solution** (backend + frontend + database)
✅ **Automatic deployments** from GitHub
✅ **Built-in databases** (PostgreSQL + Redis)
✅ **Custom domains** with SSL
✅ **Auto-scaling** based on traffic
✅ **Professional monitoring** and logs
✅ **Easy migration** to other platforms

## 📝 **Next Steps**

1. **Follow this guide** step by step
2. **Deploy backend** first
3. **Add databases** and test connections
4. **Deploy frontend** and test integration
5. **Set up custom domain** (optional)
6. **Monitor performance** and scale as needed

## 🆘 **Troubleshooting**

### Common Issues
1. **Database connection**: Check `DATABASE_URL` environment variable
2. **CORS errors**: Update `ALLOWED_HOSTS` in Django
3. **Build failures**: Check Dockerfile and requirements.txt
4. **Environment variables**: Ensure all required vars are set

### Getting Help
- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Railway Support](https://railway.app/support)

## 🎉 **You're All Set!**

After following this guide, you'll have:
- 🚀 **Live Django API** on Railway
- 🎨 **Live frontend** on Railway
- 🗄️ **PostgreSQL database** with your data
- 🔴 **Redis cache** for performance
- 🔒 **SSL certificates** and security
- 📱 **Custom domain** (optional)

**Your GoldBrella app will be live and professional!** 🎯 