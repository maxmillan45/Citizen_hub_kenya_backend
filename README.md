# Citizen Hub Kenya - Backend API

A comprehensive backend API for Kenya's civic technology platform - empowering citizens with constitutional knowledge, legal assistance, and civic participation tools.

**Live API:** https://citizen-hub-kenya-backend.onrender.com

## Features

### Authentication
- Phone number based registration and login
- JWT (JSON Web Token) authentication
- M-Pesa STK Push integration for identity verification
- Test authentication endpoint for development

### Constitution Management
- Full text search of the Constitution of Kenya 2010
- Access to all 33+ constitutional articles
- Simplified English versions of legal text
- Bilingual support (English and Swahili)

### AI Legal Assistant
- Natural language question answering
- Contextual search of constitution articles
- Conversation history tracking
- User feedback system
- Source attribution for answers

### Civic Features
- Did You Know - Kenyan history facts
- Frequently Asked Questions (FAQs)
- Parliament Scorecard - Track MP performance
- Public Events listing
- Anonymous Crime Reporting
- Voting verification status

## Tech Stack

- Django 6.0
- Django REST Framework 3.14
- Simple JWT 5.3
- PostgreSQL 15+ (Production) / SQLite (Development)
- Gunicorn 21.2
- Whitenoise 6.6
- Psycopg2 2.9
- python-dotenv 1.0
- requests 2.32
- django-cors-headers 4.3

## API Endpoints

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health/ | API health status |

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/register/ | Register new user | No |
| POST | /api/auth/login/ | Login with phone number | No |
| POST | /api/auth/test-success/ | Test login (returns JWT) | No |
| GET | /api/auth/profile/ | Get user profile | Yes |
| POST | /api/auth/logout/ | Logout user | Yes |

### M-Pesa Integration
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/stk/request/ | Initiate STK Push | No |
| POST | /api/auth/stk/query/ | Check transaction status | No |
| POST | /api/auth/stk/callback/ | M-Pesa callback URL | No |

### Constitution
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/constitution/search/?q={query} | Search articles | No |
| GET | /api/constitution/article/{number}/ | Get specific article | No |

### Chatbot
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/chatbot/ask/ | Ask legal question | Yes |
| GET | /api/chatbot/history/ | Get conversation history | Yes |
| POST | /api/chatbot/rate/ | Rate answer helpfulness | Yes |

### Civic Features
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/auth/history/ | Kenyan history facts | No |
| GET | /api/auth/history/random/ | Random history fact | No |
| GET | /api/auth/faq/ | Frequently asked questions | No |
| GET | /api/auth/mp/ | Parliament scorecard | No |
| GET | /api/auth/events/ | Public events | No |
| POST | /api/auth/crime/ | Submit crime report | Yes |
| GET | /api/auth/crime/ | Get user's reports | Yes |
| GET | /api/auth/voting/ | Voting status | No |

## Authentication

This API uses JWT (JSON Web Token) for authentication.

### Obtaining a Token

**Test Login (Development):**
```bash
curl -X POST https://citizen-hub-kenya-backend.onrender.com/api/auth/test-success/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"0705632334"}'



## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/maxmillan45/Citizen_hub_kenya_backend.git
cd Citizen_hub_kenya_backend


### Step 2: Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Step 3: Install Dependencies
bash
pip install -r requirements.txt

### Step 4: Set Up Environment Variables
Create a .env file:

bash
cat > .env << 'EOF'
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_PASSKEY=your_passkey
MPESA_SHORTCODE=174379
MPESA_ENVIRONMENT=sandbox
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok.io/api/auth/callback/
EOF


### Step 5: Run Migrations
```bash
python manage.py migrate

### Step 6: Create Superuser
bash
python manage.py createsuperuser

### Step 7: Run Server
bash
python manage.py runserver

#Testing the API
Test Health Check
bash
curl http://127.0.0.1:8000/health/

#Test Login
bash
curl -X POST http://127.0.0.1:8000/api/auth/test-success/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"0705632334"}'

#Test Constitution Search
bash
curl "http://127.0.0.1:8000/api/constitution/search/?
q=rights"

#Test Chatbot (with token)
bash
TOKEN="your_access_token_here"
curl -X POST http://127.0.0.1:8000/api/chatbot/ask/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What are my rights if arrested?","language":"en"}'

#Test M-Pesa STK Push
bash
curl -X POST http://127.0.0.1:8000/api/auth/stk/request/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"0705632334"}'


### Deployment to Render
Push code to GitHub

Log in to Render.com

Click "New +" -> "Web Service"

Connect your GitHub repository

Use these settings:

Build Command: pip install -r requirements.txt

Start Command: gunicorn citizenhub.wsgi:application

Add environment variables in Render dashboard

Click "Create Web Service"
