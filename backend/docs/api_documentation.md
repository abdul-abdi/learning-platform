# API Documentation

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

... (continue documenting other endpoints)