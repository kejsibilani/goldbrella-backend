# Railway Deployment Guide (Free Tier)

Railway offers the most generous free tier for Django apps with $5/month credit.

## 🚀 Quick Deploy

### 1. Sign Up
- Go to [railway.app](https://railway.app)
- Sign up with GitHub
- Create new project

### 2. Connect Repository
```bash
# Fork/clone your repo to GitHub first
git clone https://github.com/yourusername/goldbrella-backend
cd goldbrella-backend
```

### 3. Create Railway Configuration
Create `railway.json` in your project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 4. Deploy
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## 🗄️ Database Setup

### 1. Add PostgreSQL
- In Railway dashboard: "New Service" → "Database" → "PostgreSQL"
- Railway automatically provides connection variables

### 2. Add Redis
- "New Service" → "Database" → "Redis"
- Railway handles connection details

## ⚙️ Environment Variables

Railway automatically detects these from your `.env` file:

```bash
# Database (Railway auto-sets these)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

## 🔄 Automatic Deployments

Railway automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update for Railway deployment"
git push origin main
```

## 💰 Cost Breakdown (Free Tier)

- **$5/month credit** included
- **PostgreSQL**: ~$2-3/month
- **Redis**: ~$1-2/month
- **App hosting**: ~$0-1/month
- **Total**: Usually under $5/month (FREE!)

## 🎯 Advantages

✅ **Most generous free tier**
✅ **Automatic deployments**
✅ **Built-in PostgreSQL & Redis**
✅ **Custom domains**
✅ **SSL certificates**
✅ **No sleep/wake delays**

## 📝 Next Steps

1. **Deploy to Railway** using the guide above
2. **Set up custom domain** (optional)
3. **Configure monitoring** (Railway provides basic metrics)
4. **Scale up** when you exceed free tier

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Railway Pricing](https://railway.app/pricing)
- [Django on Railway](https://docs.railway.app/deploy/deployments/dockerfile) 