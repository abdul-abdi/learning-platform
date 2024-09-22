# Setup Guide

This guide will walk you through the process of setting up the AI-Driven Personalized Learning Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9+
- Node.js 14+
- PostgreSQL
- Redis
- Docker (optional)

## Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```
     cp .env.example .env
     ```
   - Open `.env` and set the required variables (see [Environment Variables](#environment-variables) section)

5. Initialize the database:
   ```
   flask db upgrade
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd ../frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```
     cp .env.example .env
     ```
   - Open `.env` and set `REACT_APP_API_URL` to your backend API URL (e.g., `http://localhost:5000/api`)

## Environment Variables

### Backend

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT encoding
- `REDIS_URL`: Redis connection string
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`: SMTP settings for email
- `SENTRY_DSN`: Sentry DSN for error tracking
- `FLASK_ENV`: Set to `development` or `production`
- `SECRET_KEY`: Flask secret key
- `ENCRYPTION_KEY`: Key for data encryption

### Frontend

- `REACT_APP_API_URL`: URL of your backend API

For a complete list of environment variables, refer to the `.env.example` files in both backend and frontend directories.

## Next Steps

Once you've completed the setup, you can proceed to [run the application](DEVELOPMENT.md#running-the-application).