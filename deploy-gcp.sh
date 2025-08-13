#!/bin/bash

# GCP Deployment Script for GoldBrella
# Make sure you have gcloud CLI installed and configured

set -e

# Configuration
PROJECT_ID="your-project-id"
REGION="us-central1"
SERVICE_NAME="goldbrella-backend"
DB_INSTANCE_NAME="goldbrella-db"
REDIS_INSTANCE_NAME="goldbrella-redis"

echo "🚀 Starting GCP deployment for GoldBrella..."

# Check if gcloud is configured
if ! gcloud config get-value project &> /dev/null; then
    echo "❌ gcloud CLI not configured. Please run 'gcloud auth login' and 'gcloud config set project $PROJECT_ID'"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required GCP APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    cloudresourcemanager.googleapis.com

# Create Cloud SQL instance (PostgreSQL)
echo "🗄️ Creating PostgreSQL instance..."
gcloud sql instances create $DB_INSTANCE_NAME \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup-start-time=02:00 \
    --enable-point-in-time-recovery \
    --quiet

# Create database
echo "📊 Creating database..."
gcloud sql databases create goldbrella --instance=$DB_INSTANCE_NAME --quiet

# Create database user
echo "👤 Creating database user..."
gcloud sql users create goldbrella-user \
    --instance=$DB_INSTANCE_NAME \
    --password=GoldBrella2024! \
    --quiet

# Create Redis instance
echo "🔴 Creating Redis instance..."
gcloud redis instances create $REDIS_INSTANCE_NAME \
    --size=1 \
    --region=$REGION \
    --redis-version=redis_6_x \
    --quiet

# Get connection details
DB_CONNECTION_NAME=$(gcloud sql instances describe $DB_INSTANCE_NAME --region=$REGION --format="value(connectionName)")
REDIS_HOST=$(gcloud redis instances describe $REDIS_INSTANCE_NAME --region=$REGION --format="value(host)")

echo "📝 Database connection: $DB_CONNECTION_NAME"
echo "📝 Redis host: $REDIS_HOST"

# Build and deploy to Cloud Run
echo "🐳 Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10 \
    --set-env-vars="DJANGO_SETTINGS_MODULE=goldbrella.settings" \
    --set-env-vars="DATABASE_HOST=/cloudsql/$DB_CONNECTION_NAME" \
    --add-cloudsql-instances=$DB_CONNECTION_NAME \
    --quiet

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🗄️ Database: $DB_CONNECTION_NAME"
echo "🔴 Redis: $REDIS_HOST"

# Create environment file template
echo "📝 Creating .env.production template..."
cat > .env.production << EOF
# Production Environment Variables
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=$SERVICE_URL

# Database
DATABASE_NAME=goldbrella
DATABASE_USER=goldbrella-user
DATABASE_PASSWORD=GoldBrella2024!
DATABASE_HOST=/cloudsql/$DB_CONNECTION_NAME
DATABASE_PORT=5432

# Redis
CELERY_BROKER_URL=redis://$REDIS_HOST:6379/0

# JWT
ACCESS_TOKEN_LIFETIME=300
REFRESH_TOKEN_LIFETIME=86400
ROTATE_REFRESH_TOKENS=true

# Email (configure as needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=true

# Stripe (configure as needed)
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# Site URL
SITE_URL=$SERVICE_URL
EOF

echo "📋 Next steps:"
echo "1. Update .env.production with your actual values"
echo "2. Run migrations: gcloud run jobs create migrate --image gcr.io/$PROJECT_ID/$SERVICE_NAME --command='python manage.py migrate'"
echo "3. Create superuser: gcloud run jobs create createsuperuser --image gcr.io/$PROJECT_ID/$SERVICE_NAME --command='python manage.py createsuperuser'"
echo "4. Test your API at: $SERVICE_URL/docs/" 