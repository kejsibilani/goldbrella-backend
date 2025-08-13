# QR Code Booking System API Documentation

## Overview
The QR code booking system allows for secure verification of bookings through QR codes. Each booking automatically generates a unique token and QR code that can be scanned by admin staff to verify and check-in customers.

## Features

### 1. Automatic QR Code Generation
- Every booking automatically generates a unique token and QR code
- QR codes contain verification URLs that can be scanned by admin staff
- QR codes are embedded in booking API responses

### 2. Admin QR Code Scanning
- Admin interface with QR code scanner
- Manual token input for verification
- Real-time booking verification and check-in

### 3. User QR Code Access
- Users can view their booking QR codes
- Printable QR codes for offline access
- Mobile-friendly QR code display

## API Endpoints

### 1. Get Booking QR Code (Admin)
```
GET /api/v1/bookings/{booking_id}/qr-code/
```
**Headers:** `Authorization: Bearer <token>`
**Permissions:** Admin only

**Response:**
```json
{
    "booking_id": 123,
    "qr_code": "base64_encoded_image",
    "verification_url": "https://example.com/api/v1/bookings/verify/token123/",
    "token": "token123"
}
```

### 2. Verify Booking via QR Code
```
GET /api/v1/bookings/verify/{token_key}/
```
**Headers:** `Authorization: Bearer <token>`
**Permissions:** Admin only

**Response:**
```json
{
    "valid": true,
    "message": "Booking verified successfully",
    "booking": {
        "id": 123,
        "user": {...},
        "beach": {...},
        "booking_date": "2024-01-15",
        "status": "reserved",
        ...
    }
}
```

### 3. Check-in Booking
```
POST /api/v1/bookings/verify/{token_key}/
```
**Headers:** `Authorization: Bearer <token>`
**Permissions:** Admin only

**Response:**
```json
{
    "success": true,
    "message": "Booking checked in successfully",
    "booking": {...}
}
```

### 4. Get User Booking QR Code
```
GET /api/bookings/{booking_id}/qr/
```
**Headers:** `Authorization: Bearer <token>`
**Permissions:** Booking owner or admin

**Response:** HTML page with QR code display

### 5. Get User Booking QR Code (API)
```
GET /api/bookings/{booking_id}/qr/
```
**Headers:** `Authorization: Bearer <token>`
**Permissions:** Booking owner or admin

**Response:**
```json
{
    "booking_id": 123,
    "qr_code": "base64_encoded_image",
    "verification_url": "https://example.com/api/v1/bookings/verify/token123/",
    "token": "token123"
}
```

## Admin Interface

### QR Code Scanner
- **URL:** `/admin/booking/booking/qr-scanner/`
- **Features:**
  - Camera-based QR code scanning
  - Manual token input
  - Real-time verification
  - Check-in functionality

### QR Code Display
- **URL:** `/admin/booking/booking/{id}/qr-code/`
- **Features:**
  - Individual booking QR code display
  - Printable QR codes
  - Booking details
  - Verification instructions

## Management Commands

### Generate QR Codes for Existing Bookings
```bash
python manage.py generate_booking_qr_codes
```

**Options:**
- `--output-dir`: Specify output directory (default: qr_codes)
- `--booking-id`: Generate QR code for specific booking
- `--force`: Regenerate existing QR codes

**Examples:**
```bash
# Generate QR codes for all bookings
python manage.py generate_booking_qr_codes

# Generate QR code for specific booking
python manage.py generate_booking_qr_codes --booking-id 123

# Generate QR codes in custom directory
python manage.py generate_booking_qr_codes --output-dir custom_qr_codes

# Force regenerate all QR codes
python manage.py generate_booking_qr_codes --force
```

## Frontend Integration

### 1. Display QR Code in User Interface
```javascript
// Fetch QR code data
const response = await fetch(`/api/bookings/${bookingId}/qr/`, {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
const qrData = await response.json();

// Display QR code
const img = document.createElement('img');
img.src = `data:image/png;base64,${qrData.qr_code}`;
document.getElementById('qr-container').appendChild(img);
```

### 2. QR Code Scanner Integration
```javascript
// Verify booking via token
async function verifyBooking(token) {
    const response = await fetch(`/api/v1/bookings/verify/${token}/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${adminToken}`
        }
    });
    
    const result = await response.json();
    if (result.valid) {
        // Show booking details
        displayBookingDetails(result.booking);
    } else {
        // Show error message
        showError(result.message);
    }
}
```

## Security Features

1. **Token-based Verification:** Each booking has a unique token
2. **Admin-only Verification:** Only admin users can verify bookings
3. **User Access Control:** Users can only access their own booking QR codes
4. **Secure URLs:** Verification URLs contain encrypted tokens

## Usage Workflow

### For Customers:
1. Make a booking through the system
2. Receive booking confirmation with QR code
3. Show QR code to staff upon arrival
4. Staff scans QR code to verify booking
5. Booking is marked as checked-in

### For Staff:
1. Access admin QR scanner interface
2. Scan customer's QR code or enter token manually
3. View booking details and verify authenticity
4. Check-in customer if verification successful
5. Update booking status to confirmed

## Error Handling

### Common Error Responses:
```json
{
    "valid": false,
    "message": "Invalid booking token",
    "booking": null
}
```

```json
{
    "valid": false,
    "message": "Booking has been cancelled",
    "booking": null
}
```

```json
{
    "success": false,
    "message": "Cannot check in cancelled booking"
}
```

## Dependencies

- `qrcode[pil]==7.4.2`: QR code generation
- `Pillow`: Image processing for QR codes

## Configuration

Add to your Django settings:
```python
# Site URL for QR code generation
SITE_URL = 'https://your-domain.com'

# QR code settings (optional)
QR_CODE_VERSION = 1
QR_CODE_ERROR_CORRECTION = 'L'
QR_CODE_BOX_SIZE = 10
QR_CODE_BORDER = 4
``` 