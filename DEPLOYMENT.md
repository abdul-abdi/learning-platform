# Deployment Guide

This guide covers deploying the AI-Driven Personalized Learning Platform to production environments.

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. Login to Heroku:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

3. Add PostgreSQL addon:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Add Redis addon:
   ```
   heroku addons:create heroku-redis:hobby-dev
   ```

5. Set environment variables:
   ```
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set JWT_SECRET_KEY=your_jwt_secret_key
   heroku config:set SENTRY_DSN=your_sentry_dsn
   ```
   (Add any other necessary environment variables)

6. Deploy the application:
   ```
   git push heroku main
   ```

7. Run database migrations:
   ```
   heroku run flask db upgrade
   ```

8. Ensure at least one instance of the app is running:
   ```
   heroku ps:scale web=1
   ```

## Docker Deployment

1. Build the Docker images:
   ```
   docker-compose build
   ```

2. Start the containers:
   ```
   docker-compose up -d
   ```

3. Run database migrations:
   ```
   docker-compose exec backend flask db upgrade
   ```

## CI/CD Pipeline

Our CI/CD pipeline is configured using GitHub Actions. The workflow is defined in `.github/workflows/ci-cd.yml`.

The pipeline includes the following steps:
1. Run backend tests
2. Run frontend tests
3. Run E2E tests
4. Perform load testing
5. Deploy to production (only on main branch)

To set up the CI/CD pipeline:
1. Configure the necessary secrets in your GitHub repository settings.
2. Ensure your Heroku API key is added as a secret named `HEROKU_API_KEY`.
3. Push changes to the main branch to trigger the workflow.

For more details on the CI/CD configuration, refer to the `.github/workflows/ci-cd.yml` file in the repository.