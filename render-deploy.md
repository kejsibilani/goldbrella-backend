# Render Deployment Guide (Free Tier)

Render offers a great free tier with 750 hours/month and built-in databases.

## 🚀 Quick Deploy

### 1. Sign Up
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Create new account

### 2. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Choose "Docker" as runtime

### 3. Configure Service
```
Name: goldbrella-backend
Environment: Docker
Branch: main
Build Command: (leave empty - uses Dockerfile)
Start Command: (leave empty - uses Dockerfile)
```

### 4. Environment Variables
Add these in Render dashboard:

```bash
# Django
DJANGO_SETTINGS_MODULE=goldbrella.settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.onrender.com

# Database (will be set by Render)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## 🗄️ Database Setup

### 1. Add PostgreSQL
- "New +" → "PostgreSQL"
- Choose free plan
- Copy connection string to `DATABASE_URL`

### 2. Add Redis
- "New +" → "Redis"
- Choose free plan
- Copy connection string to `REDIS_URL`

## ⚙️ Render Configuration

Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: goldbrella-backend
    env: docker
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn goldbrella.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DJANGO_SETTINGS_MODULE
        value: goldbrella.settings
      - key: DEBUG
        value: false

  - type: pserv
    name: goldbrella-db
    env: postgresql
    plan: free

  - type: pserv
    name: goldbrella-redis
    env: redis
    plan: free
```

## 🔄 Automatic Deployments

Render automatically deploys on every push:

```bash
git add .
git commit -m "Update for Render deployment"
git push origin main
```

## 💰 Cost Breakdown (Free Tier)

- **Web Service**: 750 hours/month (FREE)
- **PostgreSQL**: 750 hours/month (FREE)
- **Redis**: 750 hours/month (FREE)
- **Total**: Completely FREE!

## ⚠️ Free Tier Limitations

- **Sleep after 15 minutes** of inactivity
- **Cold start** when waking up
- **Limited bandwidth** (but generous for small apps)
- **No custom domains** on free tier

## 🎯 Advantages

✅ **Completely free** for small projects
✅ **Built-in PostgreSQL & Redis**
✅ **Automatic deployments**
✅ **SSL certificates**
✅ **Good documentation**

## 📝 Next Steps

1. **Deploy to Render** using the guide above
2. **Test your API** endpoints
3. **Monitor performance** (cold starts)
4. **Upgrade to paid** when you need custom domains

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Render Pricing](https://render.com/pricing)
- [Django on Render](https://render.com/docs/deploy-django) 