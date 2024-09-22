# AI-Driven Personalized Learning Platform - Backend

This is the backend component of our AI-Driven Personalized Learning Platform.

## 🛠️ Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env`

4. Initialize the database:
   ```
   python manage.py db upgrade
   ```

## 🚀 Running the Application

1. Start the Flask server:
   ```
   python manage.py runserver
   ```

2. Start the Celery worker:
   ```
   celery -A app.tasks worker --loglevel=info
   ```

## 🧪 Running Tests

```
pytest
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📚 References

- [Flask](https://flask.palletsprojects.com/)
- [Celery](https://docs.celeryq.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Sentry](https://sentry.io/)
- [Prometheus](https://prometheus.io/)