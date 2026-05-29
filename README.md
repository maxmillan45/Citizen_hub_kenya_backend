# Citizen Hub Kenya Backend

Django backend for Citizen Hub Kenya - A civic technology platform empowering Kenyan citizens.

## Features
- Phone number authentication
- JWT token security
- Constitution search and browse
- Bilingual support (English/Swahili)

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### Authentication
- Phone number based registration and login
- JWT access and refresh tokens
- Profile management

### Constitution Module
- Searchable Constitution of Kenya 2010
- Simplified English and Swahili versions
- 33 articles loaded (Chapter 1 and Bill of Rights)
- View count tracking for popular articles

### AI Chatbot
- Ask constitutional questions in English or Swahili
- Database search for relevant articles
- Source citations with article numbers
- Conversation history tracking
- User rating system for answers

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 6.0.4 | Web framework |
| Django REST Framework | 3.17.1 | API development |
| SimpleJWT | 5.5.1 | JWT authentication |
| SQLite | - | Development database |
| OpenAI | 1.0.0 | AI chatbot (ready for integration) |

## Setup Instructions

### Prerequisites
- Python 3.14 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/maxmillan45/Citizen_hub_kenya_backend.git
cd Citizen_hub_kenya_backend
