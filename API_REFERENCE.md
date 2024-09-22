# API Reference

This document provides details about the API endpoints available in the AI-Driven Personalized Learning Platform.

## Authentication

### Login
- **URL:** `/api/auth/login`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

### Register
- **URL:** `/api/auth/register`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "message": "User created successfully"
  }
  ```

## Learning Materials

### Get Learning Materials
- **URL:** `/api/learning-materials`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "Introduction to Machine Learning",
      "description": "Learn the basics of machine learning algorithms"
    },
    ...
  ]
  ```

### Get Specific Learning Material
- **URL:** `/api/learning-materials/<id>`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "id": 1,
    "title": "Introduction to Machine Learning",
    "description": "Learn the basics of machine learning algorithms",
    "content": "..."
  }
  ```

## User Progress

### Update User Progress
- **URL:** `/api/user-progress`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
  ```json
  {
    "material_id": 1,
    "progress": 75
  }
  ```
- **Response:**
  ```json
  {
    "message": "Progress updated successfully"
  }
  ```

### Get User Progress
- **URL:** `/api/user-progress`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  [
    {
      "material_id": 1,
      "progress": 75
    },
    ...
  ]
  ```

## Analytics

### Get User Analytics
- **URL:** `/api/analytics`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
  ```json
  {
    "total_time_spent": 3600,
    "materials_completed": 5,
    "average_quiz_score": 85
  }
  ```

For more detailed information about request/response schemas and error handling, please refer to the Swagger documentation available at `/api/docs` when running the application.