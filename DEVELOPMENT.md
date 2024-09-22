# 🚀 Development Guide

Welcome to our exciting AI-Driven Personalized Learning Platform! This guide will help you get started with running the application, understanding the project structure, and following our coding standards. Let's dive in!

## 🏃‍♂️ Running the Application

### 🖥️ Backend
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Start the Flask server:
   ```
   flask run
   ```
4. In a separate terminal, start the Celery worker:
   ```
   celery -A app.tasks worker --loglevel=info
   ```

### 🎨 Frontend
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Start the React development server:
   ```
   npm start
   ```

🎉 Congratulations! Your application should now be running at `http://localhost:3000`, with the backend API at `http://localhost:5000`. Happy coding!

## 📚 References

- [Flask](https://flask.palletsprojects.com/)
- [Celery](https://docs.celeryq.dev/)
- [React](https://reactjs.org/)
- [Redux](https://redux.js.org/)
- [React Router](https://reactrouter.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Sentry](https://sentry.io/)
- [Prometheus](https://prometheus.io/)


