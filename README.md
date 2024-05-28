
# Notion Backend

## Overview

This project is a backend system built using FastAPI. It includes features such as user authentication, lead management, and email notifications. The project uses SQLAlchemy for database interactions and Pydantic for data validation.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)

## Features

- User authentication with JWT
- Lead creation, updating, and retrieval
- Email notifications for new leads

## Getting Started

### Prerequisites

- Python 3.12
- Redis
- SQLite (default) or any other SQL database supported by SQLAlchemy

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hnikhar/notion-backend-eng.git
   cd notion-backend-end
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
 ```bash
   pip install -r requirements.txt
   ```

4. **Set up Redis:**

 ```bash
   brew install redis
  brew services start redis
   ```
## Configuration
Configuration settings are managed using environment variables. Create a `.env` file in the project root directory with the following content:
```bash
DATABASE_URL=sqlite:///./leads.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAIL_USERNAME=your_email_username
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_TLS=True
MAIL_SSL=False

```

## Running the Application
### Development Server
To run the development server:

```bash
uvicorn app.main:app --reload 
```
### Accessing the API
Once the server is running, you can access the API  at:
`http://127.0.0.1:8000/`

### API Endpoints
### Authentication
 ``` bash
POST /token: Obtain a JWT token by providing username and password.
```
### Users
``` bash
GET /users/me/: Retrieve the current authenticated user.
```
### Leads
``` bash
POST /leads: Create a new lead.
GET /leads: Retrieve all leads.
PATCH /leads/{lead_id}: Update an existing lead.
```
## Environment Variables
The project uses a `.env` file to manage environment variables securely. Ensure the `.env` file is included in your `.gitignore` to prevent sensitive information from being committed to your version control system:
```bash
# .gitignore
.env
```








