# Citizen Hub Kenya API - Postman Collection

## Files Included

1. `Citizen_Hub_Kenya_Postman_Collection.json` - Complete API collection
2. `Citizen_Hub_Kenya_Environment.json` - Local development environment
3. `Citizen_Hub_Kenya_Production_Environment.json` - Production environment

## How to Import

### Import Collection
1. Open Postman
2. Click "Import" button
3. Select `Citizen_Hub_Kenya_Postman_Collection.json`
4. Click "Import"

### Import Environment
1. Click "Environments" in left sidebar
2. Click "Import"
3. Select `Citizen_Hub_Kenya_Environment.json`
4. Click "Import"
5. Repeat for production environment

## How to Use

### Local Development
1. Start your Django server: `python manage.py runserver`
2. In Postman, select "Citizen Hub Kenya" environment from dropdown
3. Register a user using the Register endpoint
4. Login to get access_token (automatically save to environment)

### Authentication Flow
1. Call `POST /api/auth/register/` to create account
2. Call `POST /api/auth/login/` to get tokens
3. Copy `access_token` to environment variable
4. All authenticated endpoints will use this token

### Admin Access
1. Create superuser: `python manage.py createsuperuser`
2. Login with superuser credentials
3. Copy admin token to `admin_access_token` variable

## API Categories

- **Authentication** - Register, login, profile, password management
- **Kenyan History** - Historical facts with pagination and filtering
- **FAQs** - Citizen questions with CRUD operations
- **Members of Parliament** - MP data with search and filters
- **Public Events** - Civic events and gatherings
- **Crime Reporting** - Submit and track crime reports
- **Constitution** - Search and view constitution articles
- **Chatbot** - AI legal assistant
- **M-Pesa** - Mobile payments integration
- **Voting** - User voting records
- **Admin Monitoring** - Dashboard, user management, analytics
- **Data Scraping** - Trigger data updates (admin only)
- **Utility** - Health check, documentation

## Testing Workflow

1. Start with Health Check to verify server is running
2. Register a new user
3. Login to get tokens
4. Test authenticated endpoints (Crime reports, Chatbot, etc.)
5. Create admin user and test admin endpoints

## Variables

Environment variables used:
- `base_url` - API base URL
- `access_token` - JWT token for normal users
- `admin_access_token` - JWT token for admin users
- `refresh_token` - Token for refreshing access
- `user_id`, `faq_id`, `mp_id`, etc. - IDs for testing

## Common Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource does not exist
- `500 Internal Server Error` - Server error

## Running Tests

Use Postman's Collection Runner:
1. Click "Runner" button
2. Select Citizen Hub Kenya collection
3. Select environment
4. Click "Run"

## Support

For issues, check:
- Server logs: `logs/django.log`
- Django admin: `/admin`
- API docs: `/swagger/` or `/redoc/`
