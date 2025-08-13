# GCP Deployment Guide for GoldBrella

This guide will walk you through deploying your GoldBrella Django backend on Google Cloud Platform (GCP).

## Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud CLI**: Install and configure [gcloud CLI](https://cloud.google.com/sdk/docs/install)
3. **Docker**: Install [Docker](https://docs.docker.com/get-docker/) (for local testing)

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React/Vue)   │◄──►│   (Cloud Run)   │◄──►│   (Cloud SQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis         │
                       │   (Memorystore) │
                       └─────────────────┘
```

## Step 1: Project Setup

### 1.1 Create GCP Project

```bash
# Create new project
gcloud projects create goldbrella-app --name="GoldBrella Application"

# Set as active project
gcloud config set project goldbrella-app

# Enable billing (required for Cloud SQL and other services)
# Go to: https://console.cloud.google.com/billing
```

### 1.2 Enable Required APIs

```bash
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    cloudresourcemanager.googleapis.com \
    compute.googleapis.com
```

## Step 2: Database Setup (Cloud SQL)

### 2.1 Create PostgreSQL Instance

```bash
gcloud sql instances create goldbrella-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup-start-time=02:00 \
    --enable-point-in-time-recovery \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=02
```

### 2.2 Create Database and User

```bash
# Create database
gcloud sql databases create goldbrella --instance=goldbrella-db

# Create user
gcloud sql users create goldbrella-user \
    --instance=goldbrella-db \
    --password=YourStrongPassword123!

# Get connection info
gcloud sql instances describe goldbrella-db --region=us-central1
```

## Step 3: Redis Setup (Memorystore)

### 3.1 Create Redis Instance

```bash
gcloud redis instances create goldbrella-redis \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x \
    --tier=BASIC
```

### 3.2 Get Redis Connection Details

```bash
gcloud redis instances describe goldbrella-redis --region=us-central1
```

## Step 4: Backend Deployment (Cloud Run)

### 4.1 Build and Deploy

```bash
# Deploy to Cloud Run
gcloud run deploy goldbrella-backend \
    --source . \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10 \
    --set-env-vars="DJANGO_SETTINGS_MODULE=goldbrella.settings" \
    --set-env-vars="DATABASE_HOST=/cloudsql/PROJECT_ID:us-central1:goldbrella-db" \
    --add-cloudsql-instances=PROJECT_ID:us-central1:goldbrella-db
```

**Replace `PROJECT_ID` with your actual project ID.**

### 4.2 Environment Variables

Create a `.env.production` file with:

```bash
# Production Environment Variables
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=your-cloud-run-url.run.app

# Database
DATABASE_NAME=goldbrella
DATABASE_USER=goldbrella-user
DATABASE_PASSWORD=YourStrongPassword123!
DATABASE_HOST=/cloudsql/PROJECT_ID:us-central1:goldbrella-db
DATABASE_PORT=5432

# Redis
CELERY_BROKER_URL=redis://REDIS_IP:6379/0

# JWT
ACCESS_TOKEN_LIFETIME=300
REFRESH_TOKEN_LIFETIME=86400
ROTATE_REFRESH_TOKENS=true

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=true

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Site URL
SITE_URL=https://your-cloud-run-url.run.app
```

## Step 5: Database Migration

### 5.1 Run Migrations

```bash
# Create a Cloud Run job for migrations
gcloud run jobs create migrate \
    --image gcr.io/PROJECT_ID/goldbrella-backend \
    --region=us-central1 \
    --command="python manage.py migrate" \
    --set-env-vars="DATABASE_HOST=/cloudsql/PROJECT_ID:us-central1:goldbrella-db" \
    --add-cloudsql-instances=PROJECT_ID:us-central1:goldbrella-db

# Execute the job
gcloud run jobs execute migrate --region=us-central1
```

### 5.2 Create Superuser

```bash
# Create superuser job
gcloud run jobs create createsuperuser \
    --image gcr.io/PROJECT_ID/goldbrella-backend \
    --region=us-central1 \
    --command="python manage.py createsuperuser" \
    --set-env-vars="DATABASE_HOST=/cloudsql/PROJECT_ID:us-central1:goldbrella-db" \
    --add-cloudsql-instances=PROJECT_ID:us-central1:goldbrella-db

# Execute the job
gcloud run jobs execute createsuperuser --region=us-central1
```

## Step 6: Frontend Deployment

### 6.1 Build Frontend

```bash
# Navigate to frontend directory
cd ../goldbrella-frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 6.2 Deploy to Cloud Storage + Load Balancer

```bash
# Create bucket
gsutil mb gs://goldbrella-frontend

# Upload build files
gsutil -m cp -r dist/* gs://goldbrella-frontend/

# Make bucket public
gsutil iam ch allUsers:objectViewer gs://goldbrella-frontend

# Create load balancer (optional, for custom domain)
# This requires additional setup with Cloud DNS
```

## Step 7: Domain and SSL

### 7.1 Custom Domain Setup

```bash
# Create Cloud DNS zone
gcloud dns managed-zones create goldbrella-zone \
    --dns-name="yourdomain.com." \
    --description="GoldBrella DNS zone"

# Add DNS records
gcloud dns record-sets transaction start --zone=goldbrella-zone
gcloud dns record-sets transaction add \
    --zone=goldbrella-zone \
    --name="api.yourdomain.com." \
    --type=A \
    --ttl=300 \
    "CLOUD_RUN_IP"
gcloud dns record-sets transaction execute --zone=goldbrella-zone
```

### 7.2 SSL Certificate

```bash
# Cloud Run automatically provides SSL certificates
# For custom domains, you'll need to verify domain ownership
```

## Step 8: Monitoring and Logging

### 8.1 Enable Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# Enable Cloud Logging
gcloud services enable logging.googleapis.com
```

### 8.2 Set Up Alerts

```bash
# Create uptime check
gcloud monitoring uptime-checks create http goldbrella-health \
    --display-name="GoldBrella Health Check" \
    --uri="https://your-api-url/health/" \
    --period=60s
```

## Step 9: CI/CD Pipeline

### 9.1 Connect GitHub Repository

```bash
# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Grant Cloud Build access to your repository
# Go to: https://console.cloud.google.com/cloud-build/triggers
```

### 9.2 Create Build Trigger

```bash
# Create trigger
gcloud builds triggers create github \
    --repo-name=goldbrella-backend \
    --repo-owner=your-username \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml
```

## Step 10: Testing

### 10.1 Health Check

```bash
# Test your API
curl https://your-cloud-run-url.run.app/health/
```

### 10.2 API Documentation

```bash
# Access Swagger docs
open https://your-cloud-run-url.run.app/docs/
```

## Cost Optimization

### 10.1 Database

- Use `db-f1-micro` for development
- Scale to `db-n1-standard-1` for production
- Enable automatic backups

### 10.2 Cloud Run

- Set appropriate memory limits
- Use min instances for consistent performance
- Monitor usage and adjust resources

### 10.3 Redis

- Start with `BASIC` tier
- Scale based on usage patterns

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure Cloud SQL proxy is configured
2. **Environment Variables**: Check all required vars are set
3. **Permissions**: Verify service account permissions
4. **CORS**: Update CORS settings for your frontend domain

### Useful Commands

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=goldbrella-backend" --limit=50

# Check service status
gcloud run services describe goldbrella-backend --region=us-central1

# View database logs
gcloud sql logs tail --instance=goldbrella-db
```

## Security Best Practices

1. **Secrets Management**: Use Secret Manager for sensitive data
2. **Network Security**: Use VPC connectors for private networking
3. **IAM**: Follow principle of least privilege
4. **Monitoring**: Set up security monitoring and alerts

## Next Steps

1. Set up monitoring and alerting
2. Configure backup strategies
3. Implement CI/CD pipeline
4. Set up staging environment
5. Configure custom domain and SSL
6. Set up monitoring dashboards

## Support

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Memorystore Documentation](https://cloud.google.com/memorystore/docs)
- [Cloud Build Documentation](https://cloud.google.com/cloud-build/docs) 