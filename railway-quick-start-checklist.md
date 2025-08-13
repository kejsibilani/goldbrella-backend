# Railway Quick Start Checklist 🚀

Follow this checklist to deploy your complete GoldBrella solution on Railway in under 30 minutes!

## ✅ **Pre-Deployment Checklist**

- [ ] **GitHub repository** ready with your code
- [ ] **Railway account** created at [railway.app](https://railway.app)
- [ ] **Dockerfile** exists in your project (✅ Already created!)
- [ ] **requirements.txt** updated with gunicorn (✅ Already done!)
- [ ] **Frontend code** ready (React/Vue app)

## 🚀 **Step 1: Create Railway Project (5 min)**

- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up with GitHub
- [ ] Click **"New Project"**
- [ ] Name: `goldbrella`
- [ ] Click **"Deploy from GitHub repo"**

## 🐍 **Step 2: Deploy Backend (10 min)**

- [ ] **Select your backend repository**
- [ ] Railway auto-detects Dockerfile ✅
- [ ] **Service name**: `goldbrella-backend`
- [ ] **Wait for build** (usually 2-3 minutes)
- [ ] **Copy your backend URL** (e.g., `https://goldbrella-backend-xxxx.railway.app`)

## 🗄️ **Step 3: Add Databases (5 min)**

- [ ] **Add PostgreSQL**:
  - [ ] Click **"Add Service"** → **"Database"** → **"PostgreSQL"**
  - [ ] Name: `goldbrella-db`
  - [ ] Railway auto-sets `DATABASE_URL` ✅

- [ ] **Add Redis**:
  - [ ] Click **"Add Service"** → **"Database"** → **"Redis"**
  - [ ] Name: `goldbrella-redis`
  - [ ] Railway auto-sets `REDIS_URL` ✅

## ⚙️ **Step 4: Configure Environment Variables (5 min)**

- [ ] **Go to backend service** → **Variables**
- [ ] **Add these variables**:

```bash
DJANGO_SETTINGS_MODULE=goldbrella.settings
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=.railway.app
ACCESS_TOKEN_LIFETIME=300
REFRESH_TOKEN_LIFETIME=86400
ROTATE_REFRESH_TOKENS=true
SITE_URL=https://your-backend-url.railway.app
```

## 🎨 **Step 5: Deploy Frontend (10 min)**

- [ ] **Add Static Site Service**:
  - [ ] Click **"Add Service"** → **"Static Site"**
  - [ ] Connect your frontend repository
  - [ ] **Build Command**: `npm run build`
  - [ ] **Publish Directory**: `dist` (Vue) or `build` (React)
  - [ ] **Install Command**: `npm install`

- [ ] **Add Frontend Environment Variables**:
```bash
VITE_API_BASE_URL=https://your-backend-url.railway.app
# OR for React:
REACT_APP_API_BASE_URL=https://your-backend-url.railway.app
```

## 🔄 **Step 6: Database Setup (5 min)**

- [ ] **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

- [ ] **Run migrations**:
```bash
railway login
railway link
railway run python manage.py migrate
```

- [ ] **Create superuser**:
```bash
railway run python manage.py createsuperuser
```

## 🧪 **Step 7: Test Everything (5 min)**

- [ ] **Test Backend API**:
  - [ ] Open: `https://your-backend-url.railway.app/docs/`
  - [ ] Test a few API endpoints

- [ ] **Test Frontend**:
  - [ ] Open your frontend URL
  - [ ] Test API connections
  - [ ] Verify all features work

- [ ] **Test Database**:
  - [ ] Check admin panel: `https://your-backend-url.railway.app/admin/`
  - [ ] Login with superuser credentials

## 🌐 **Step 8: Custom Domain (Optional - 5 min)**

- [ ] **Add custom domain to backend**:
  - [ ] Go to backend service → **Settings** → **Custom Domains**
  - [ ] Add: `api.yourdomain.com`

- [ ] **Add custom domain to frontend**:
  - [ ] Go to frontend service → **Settings** → **Custom Domains**
  - [ ] Add: `www.yourdomain.com`

- [ ] **Update DNS records** at your domain provider

## 🎯 **Final Checklist**

- [ ] ✅ **Backend deployed** and accessible
- [ ] ✅ **Frontend deployed** and connected to backend
- [ ] ✅ **Database working** with data
- [ ] ✅ **Redis working** for caching
- [ ] ✅ **API endpoints** responding
- [ ] ✅ **Admin panel** accessible
- [ ] ✅ **Custom domains** working (if added)

## 🎉 **You're Live!**

**Your GoldBrella app is now deployed on Railway with:**
- 🚀 **Backend**: Django API with all your apps
- 🎨 **Frontend**: React/Vue app connected to backend
- 🗄️ **Database**: PostgreSQL with your data
- 🔴 **Redis**: Caching and Celery tasks
- 🔒 **SSL**: Automatic HTTPS
- 🌐 **Custom domains** (optional)

## 📊 **Monitor & Scale**

- [ ] **Check Railway dashboard** for metrics
- [ ] **Monitor logs** for any issues
- [ ] **Scale resources** as needed
- [ ] **Set up alerts** for downtime

## 🆘 **Need Help?**

- **Railway Docs**: [docs.railway.app](https://docs.railway.app/)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Railway Support**: [railway.app/support](https://railway.app/support)

---

**Total Time: ~30 minutes** ⏱️
**Cost: FREE** (within $5/month credit) 🆓
**Result: Professional, scalable app** 🎯 