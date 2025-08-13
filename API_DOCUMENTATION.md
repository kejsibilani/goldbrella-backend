# GoldBrella API Documentation

## Overview
GoldBrella is a sunbed booking platform API that provides comprehensive functionality for managing beach bookings, sunbeds, payments, and user management.

## Base URL
```
http://localhost:8000/api/v1/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### Authentication & User Management

#### Login
- **POST** `/login`
- **Description**: Authenticate user and get JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Register
- **POST** `/register`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
  }
  ```

#### Refresh Token
- **POST** `/refresh`
- **Description**: Get new access token using refresh token
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Verify Token
- **POST** `/verify`
- **Description**: Verify if access token is valid
- **Request Body**:
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### Logout
- **POST** `/logout`
- **Description**: Blacklist refresh token
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

#### User Profile
- **GET** `/profile` - Get current user profile
- **PUT** `/profile` - Update current user profile
- **DELETE** `/profile` - Deactivate current user account

#### Users Management
- **GET** `/users` - List users (admin/staff only)
- **GET** `/users/{id}` - Get specific user details
- **PUT** `/users/{id}` - Update user
- **DELETE** `/users/{id}` - Delete user

#### Password Reset
- **POST** `/reset-password` - Request password reset
- **POST** `/reset-password/confirm` - Confirm password reset

### Beach Management

#### Beaches
- **GET** `/beaches` - List all beaches
- **POST** `/beaches` - Create new beach (admin only)
- **GET** `/beaches/{id}` - Get specific beach details
- **PUT** `/beaches/{id}` - Update beach
- **DELETE** `/beaches/{id}` - Delete beach

#### Beach Images
- **GET** `/beach-images` - List beach images
- **POST** `/beach-images` - Upload beach image
- **GET** `/beach-images/{id}` - Get specific image
- **PUT** `/beach-images/{id}` - Update image
- **DELETE** `/beach-images/{id}` - Delete image

#### Beach Opening Hours
- **GET** `/beach-opening-hours` - List opening hours
- **POST** `/beach-opening-hours` - Create opening hours
- **GET** `/beach-opening-hours/{id}` - Get specific opening hours
- **PUT** `/beach-opening-hours/{id}` - Update opening hours

#### Beach Opening Seasons
- **GET** `/beach-opening-seasons` - List opening seasons
- **POST** `/beach-opening-seasons` - Create opening season
- **GET** `/beach-opening-seasons/{id}` - Get specific season
- **PUT** `/beach-opening-seasons/{id}` - Update season

### Zone Management

#### Zones
- **GET** `/zones` - List all zones
- **GET** `/zones/{id}` - Get specific zone details
- **PUT** `/zones/{id}` - Update zone

### Sunbed Management

#### Sunbeds
- **GET** `/sunbeds` - List all sunbeds
- **POST** `/sunbeds` - Create new sunbed
- **GET** `/sunbeds/{id}` - Get specific sunbed
- **PUT** `/sunbeds/{id}` - Update sunbed
- **DELETE** `/sunbeds/{id}` - Delete sunbed

### Booking Management

#### Bookings
- **GET** `/bookings` - List user's bookings
- **POST** `/bookings` - Create new booking
- **GET** `/bookings/{id}` - Get specific booking
- **PUT** `/bookings/{id}` - Update booking
- **DELETE** `/bookings/{id}` - Cancel booking

#### Anonymous Bookings
- **POST** `/anonymous/bookings` - Create anonymous booking
- **GET** `/anonymous/bookings?token={token}` - Get anonymous booking
- **PUT** `/anonymous/bookings?token={token}` - Update anonymous booking
- **DELETE** `/anonymous/bookings?token={token}` - Cancel anonymous booking

#### Booking History
- **GET** `/bookings/locations` - Get booking history by location
- **GET** `/bookings/beaches` - Get booking history by beach

### Inventory Management

#### Inventory Items
- **GET** `/inventory-items` - List inventory items
- **POST** `/inventory-items` - Create inventory item
- **GET** `/inventory-items/{id}` - Get specific item
- **PUT** `/inventory-items/{id}` - Update item
- **DELETE** `/inventory-items/{id}` - Delete item

### Payment Management

#### Payments
- **GET** `/payments` - List payments
- **POST** `/payments` - Create payment
- **GET** `/payments/{id}` - Get specific payment
- **POST** `/payments/{id}/mark-paid` - Mark payment as successful (staff only)

### Invoice Management

#### Invoices
- **GET** `/invoices` - List invoices
- **GET** `/invoices/{id}` - Get specific invoice
- **PUT** `/invoices/{id}` - Update invoice

### Services Management

#### Facilities
- **GET** `/facilities` - List facilities
- **POST** `/facilities` - Create facility
- **GET** `/facilities/{id}` - Get specific facility
- **PUT** `/facilities/{id}` - Update facility
- **DELETE** `/facilities/{id}` - Delete facility

#### Rules
- **GET** `/rules` - List rules
- **POST** `/rules` - Create rule
- **GET** `/rules/{id}` - Get specific rule
- **PUT** `/rules/{id}` - Update rule
- **DELETE** `/rules/{id}` - Delete rule

### Location Management

#### Locations
- **GET** `/locations` - List locations
- **POST** `/locations` - Create location
- **GET** `/locations/{id}` - Get specific location
- **PUT** `/locations/{id}` - Update location
- **DELETE** `/locations/{id}` - Delete location

### User Feedback

#### Reviews
- **GET** `/reviews` - List reviews
- **POST** `/reviews` - Create review
- **GET** `/reviews/{id}` - Get specific review
- **PUT** `/reviews/{id}` - Update review
- **DELETE** `/reviews/{id}` - Delete review

#### Complaints
- **GET** `/complaints` - List complaints
- **POST** `/complaints` - Create complaint
- **GET** `/complaints/{id}` - Get specific complaint
- **PUT** `/complaints/{id}` - Update complaint
- **DELETE** `/complaints/{id}` - Delete complaint

### Staff Management

#### Shifts
- **GET** `/shifts` - List shifts
- **GET** `/shifts/{id}` - Get specific shift
- **PUT** `/shifts/{id}` - Update shift

### Notifications

#### Notifications
- **GET** `/notifications` - List user notifications
- **GET** `/notifications/{id}` - Get specific notification
- **PATCH** `/notifications/{id}/mark-read` - Mark notification as read

### System Management

#### Scheduled Emails
- **GET** `/scheduled-emails` - List scheduled emails (admin/staff only)
- **GET** `/scheduled-emails/{id}` - Get specific scheduled email

## Query Parameters

### Pagination
All list endpoints support pagination:
```
?page=1&page_size=10
```

### Filtering
Most endpoints support filtering:
```
?field=value&another_field=value
```

### Search
Many endpoints support search:
```
?search=search_term
```

### Date Filtering
For date-based endpoints:
```
?booking_date=2024-01-15
?start_date=2024-01-01&end_date=2024-01-31
```

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

### Common HTTP Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **500** - Internal Server Error

## Rate Limiting
- Anonymous users: 150 requests per minute
- Authenticated users: 200 requests per minute

## CORS Configuration
The API is configured to allow cross-origin requests from the frontend application.

## Webhook Endpoints

### Stripe Webhook
- **POST** `/stripe/webhook/`
- **Description**: Handle Stripe payment webhooks
- **Authentication**: Uses Stripe signature verification

## Testing the API

### Using the Test Script
Run the provided test script to verify all endpoints:
```bash
python test_api_endpoints.py
```

### Using Swagger Documentation
Access the interactive API documentation at:
```
http://localhost:8000/api/docs
```

## Frontend Integration

### CORS Headers
The API includes the following CORS headers for frontend integration:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Authorization, Content-Type, Accept, Origin, X-Requested-With`
- `Access-Control-Allow-Credentials: true`

### Authentication Flow
1. User registers/logs in via `/login` or `/register`
2. Frontend stores JWT tokens securely
3. Include `Authorization: Bearer <access_token>` in API requests
4. Use `/refresh` to get new access tokens when they expire
5. Use `/logout` to invalidate refresh tokens

### Example Frontend Integration
```javascript
// Login
const response = await fetch('/api/v1/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { access, refresh } = await response.json();

// Make authenticated request
const bookingsResponse = await fetch('/api/v1/bookings', {
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json',
  }
});
```

## Environment Variables

Make sure to set the following environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (true/false)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_*` - Database configuration
- `EMAIL_*` - Email configuration
- `STRIPE_*` - Stripe configuration
- `CELERY_BROKER_URL` - Celery broker URL

## Deployment

### Docker
Use the provided `docker-compose.yml` for containerized deployment:
```bash
docker-compose up -d
```

### Manual Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver` 