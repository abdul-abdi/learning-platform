# AI-Driven Personalized Learning Platform

## Overview
This project is an AI-driven personalized learning platform that adapts to individual user needs and learning styles. It provides customized learning materials, progress tracking, and personalized recommendations.

## Features
- User authentication and authorization with JWT
- Personalized dashboard
- Adaptive learning materials
- Progress tracking
- Quiz system
- AI-powered recommendations
- Analytics and reporting
- Rate limiting
- Caching

## Tech Stack
- Backend: Flask (Python)
- Frontend: React.js
- Database: PostgreSQL
- Cache and Message Queue: Redis
- Task Queue: Celery
- Testing: Pytest, Jest, Cypress
- CI/CD: GitHub Actions
- Containerization: Docker
- Monitoring: Sentry, Prometheus

## Setup

### Prerequisites
- Python 3.9+
- Node.js 14+
- PostgreSQL
- Redis
- Docker (optional)

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
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
   - Copy `.env.example` to `.env` and fill in the required values:
     ```
     cp .env.example .env
     ```
   - Open `.env` and set the following variables:
     - DATABASE_URL: PostgreSQL connection string (e.g., postgresql://user:password@localhost:5432/dbname)
     - JWT_SECRET_KEY: Generate a secure random string (e.g., use `openssl rand -hex 32`)
     - REDIS_URL: Redis connection string (e.g., redis://localhost:6379/0)
     - SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD: Get from your email service provider
     - SENTRY_DSN: Get from your Sentry account
     - SECRET_KEY: Generate a secure random string for Flask
     - ENCRYPTION_KEY: Generate a secure random string for data encryption

5. Initialize the database:
   ```
   flask db upgrade
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
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
   - Open `.env` and set:
     - REACT_APP_API_URL: URL of your backend API (e.g., http://localhost:5000/api)

## Running the Application

### Backend
1. Start the Flask server:
   ```
   cd backend
   flask run
   ```
2. In a separate terminal, start the Celery worker:
   ```
   cd backend
   celery -A app.tasks worker --loglevel=info
   ```

### Frontend
1. Start the React development server:
   ```
   cd frontend
   npm start
   ```

The application should now be running at `http://localhost:3000`, with the backend API at `http://localhost:5000`.

## Running Tests

### Backend Tests
```
cd backend
pytest
```

### Frontend Tests
```
cd frontend
npm test
```

### E2E Tests
```
cd frontend
npm run cypress:open
```

## Load Testing
To run load tests using Locust:
```
cd backend
locust -f locustfile.py
```
Then open `http://localhost:8089` in your browser to access the Locust web interface.

## Deployment

This project is set up for continuous deployment to Heroku using GitHub Actions. However, you can also deploy manually if needed.

### Heroku Setup

1. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

2. Add PostgreSQL addon:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Add Redis addon:
   ```
   heroku addons:create heroku-redis:hobby-dev
   ```

4. Set up Heroku config vars:
   ```
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set JWT_SECRET_KEY=your_jwt_secret_key
   heroku config:set SENTRY_DSN=your_sentry_dsn
   ```
   (Add any other necessary environment variables)

### GitHub Secrets

To enable the GitHub Actions workflow to deploy to Heroku, you need to add the following secret to your GitHub repository:

1. Go to your GitHub repository settings
2. Click on "Secrets" in the left sidebar
3. Click "New repository secret"
4. Add a secret named `HEROKU_API_KEY` with your Heroku API key as the value

You can find your Heroku API key in your Heroku account settings.

### Manual Deployment

If you need to deploy manually, follow these steps:

1. Install the Heroku CLI and log in:
   ```
   heroku login
   ```

2. Add the Heroku remote to your git repository:
   ```
   heroku git:remote -a your-app-name
   ```

3. Push your code to Heroku:
   ```
   git push heroku main
   ```

4. Run database migrations:
   ```
   heroku run flask db upgrade
   ```

5. Ensure at least one instance of the app is running:
   ```
   heroku ps:scale web=1
   ```

6. Open the deployed app in your browser:
   ```
   heroku open
   ```

### Troubleshooting

If you encounter issues during deployment:

1. Check your logs:
   ```
   heroku logs --tail
   ```

2. Ensure all config vars are set correctly:
   ```
   heroku config
   ```

3. If you've made changes to your database models, make sure to run migrations:
   ```
   heroku run flask db upgrade
   ```

4. If you're using a Procfile, ensure it's configured correctly for both web and worker processes.

## Docker Support

To run the application using Docker:

1. Build the Docker images:
   ```
   docker-compose build
   ```

2. Start the containers:
   ```
   docker-compose up
   ```

The application will be available at `http://localhost:3000`, and the API at `http://localhost:5000`.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.