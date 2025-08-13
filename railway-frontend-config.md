# Frontend Deployment to Railway Static Hosting

This guide shows you exactly how to deploy your frontend to Railway's static hosting service.

## 🎨 **Frontend Deployment Options**

### **Option 1: Railway Static Hosting (Recommended)**
- ✅ **Same platform** as your backend
- ✅ **Automatic deployments** from GitHub
- ✅ **Custom domains** support
- ✅ **SSL certificates** included
- ✅ **Global CDN** for fast loading

### **Option 2: Vercel (Alternative)**
- ✅ **Excellent performance** for React/Vue
- ✅ **Generous free tier**
- ✅ **Automatic deployments**
- ❌ **Separate platform** from backend

## 🚀 **Railway Static Hosting Setup**

### **Step 1: Add Static Site Service**
1. In your Railway project dashboard
2. Click **"Add Service"**
3. Select **"Static Site"**
4. Connect your frontend GitHub repository

### **Step 2: Configure Build Settings**
Set these in Railway dashboard:

```bash
# Build Command
npm run build

# Publish Directory
dist          # (for Vite/Vue)
# OR
build         # (for Create React App)

# Install Command
npm install

# Node Version
18.x          # (or your preferred version)
```

### **Step 3: Environment Variables**
Add these for your frontend:

```bash
# API Base URL (your backend Railway URL)
VITE_API_BASE_URL=https://your-backend-name.railway.app
# OR for React
REACT_APP_API_BASE_URL=https://your-backend-name.railway.app

# App Configuration
VITE_APP_NAME=GoldBrella
VITE_APP_VERSION=1.0.0

# Stripe (if using)
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Other services
VITE_SENTRY_DSN=your-sentry-dsn
```

## 🔧 **Frontend Code Updates**

### **Update API Configuration**
Ensure your frontend can connect to the Railway backend:

```javascript
// src/config/api.js or similar
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiConfig = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
};

// API calls
export const apiClient = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    return response.json();
  },
  
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }
};
```

### **Update CORS Settings**
In your Django backend, ensure CORS allows your frontend domain:

```python
# In Django settings
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-name.railway.app",
    "https://yourdomain.com",  # if using custom domain
]

# Or allow all Railway domains
CORS_ALLOWED_ORIGINS = [
    "https://*.railway.app",
]
```

## 🌐 **Custom Domain Setup**

### **Add Custom Domain to Frontend**
1. Go to your frontend service settings
2. **Custom Domains** → **Add Domain**
3. Enter your domain (e.g., `www.yourdomain.com`)
4. Follow DNS setup instructions

### **DNS Configuration**
Add these records to your domain provider:

```bash
# Frontend
Type: CNAME
Name: www
Value: your-frontend-name.railway.app

# Backend API
Type: CNAME
Name: api
Value: your-backend-name.railway.app
```

## 📱 **Frontend Framework Specific Setup**

### **Vue.js (Vite)**
```bash
# Build command
npm run build

# Publish directory
dist

# Environment variables
VITE_API_BASE_URL=https://your-backend.railway.app
```

### **React (Create React App)**
```bash
# Build command
npm run build

# Publish directory
build

# Environment variables
REACT_APP_API_BASE_URL=https://your-backend.railway.app
```

### **Next.js**
```bash
# Build command
npm run build

# Publish directory
.next

# Note: Next.js might need custom configuration for static export
```

## 🔄 **Automatic Deployments**

### **GitHub Integration**
Railway automatically deploys when you push:

```bash
# Make changes to your frontend
git add .
git commit -m "Update frontend for Railway deployment"
git push origin main

# Railway automatically builds and deploys! 🚀
```

### **Deployment Triggers**
- ✅ **Push to main branch** → Auto-deploy
- ✅ **Pull request merge** → Auto-deploy
- ✅ **Manual deployment** → Available in dashboard

## 🧪 **Testing Your Frontend**

### **Test Local Development**
```bash
# Start development server
npm run dev

# Test API connections
# Ensure your frontend can reach your Railway backend
```

### **Test Production Build**
```bash
# Build locally
npm run build

# Test build output
# Check that all assets are generated correctly
```

### **Test Live Deployment**
1. Open your Railway frontend URL
2. Test all features and API calls
3. Verify performance and loading
4. Check mobile responsiveness

## 📊 **Monitoring & Performance**

### **Railway Dashboard**
- **Build logs**: See build process and errors
- **Deployment history**: Track all deployments
- **Performance metrics**: Monitor loading times

### **Frontend Performance**
- **Lighthouse scores**: Test performance, accessibility, SEO
- **Bundle analysis**: Check bundle sizes
- **Loading times**: Monitor real user performance

## 🎯 **Best Practices**

### **Build Optimization**
```bash
# Use production builds
npm run build

# Minimize bundle size
# Use code splitting
# Optimize images and assets
```

### **Environment Management**
```bash
# Use environment variables for configuration
# Never commit sensitive data
# Use different configs for dev/staging/prod
```

### **Error Handling**
```javascript
// Handle API errors gracefully
try {
  const data = await apiClient.get('/api/endpoint/');
  // Handle success
} catch (error) {
  // Handle error gracefully
  console.error('API Error:', error);
  // Show user-friendly error message
}
```

## 🆘 **Troubleshooting**

### **Common Issues**
1. **Build failures**: Check Node.js version and dependencies
2. **API connection errors**: Verify CORS and environment variables
3. **Asset loading issues**: Check publish directory configuration
4. **Environment variables**: Ensure all required vars are set

### **Getting Help**
- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Frontend Framework Docs](https://vuejs.org/, https://reactjs.org/)

## 🎉 **You're Ready!**

After following this guide:
- 🎨 **Frontend deployed** on Railway
- 🔗 **Connected to backend** API
- 🌐 **Custom domain** (optional)
- 🔒 **SSL certificates** included
- 📱 **Responsive design** working
- 🚀 **Fast loading** with CDN

**Your complete GoldBrella app is now live!** 🎯 