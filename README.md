# Social Networking API

This project is a social networking API built with Django and Django Rest Framework, using JWT for authentication. The API allows users to sign up, log in, search for other users, send and manage friend requests, and list friends and pending friend requests.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```bash
    git https://github.com/arun-nextbrain/social_network.git
    ```

2. Navigate to the project directory:
    ```bash
    cd social_network
    ```

3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image for the Django application and start the containers.

4. Access the application:
    Once the containers are up and running, you can access the application at [http://localhost:8000](http://localhost:8000).

## Usage

### Access the API

The API will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### Signup

- **URL:** `/api/signup/`
- **Method:** `POST`
- **Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```

### Login

- **URL:** `/api/login/`
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
        "refresh": "refresh_token",
        "access": "access_token"
    }
    ```

### Search Users

- **URL:** `/api/search/`
- **Method:** `GET`
- **Headers:**
    - `Authorization: Bearer <your-access-token>`
- **Parameters:**
    - `q`: Search query

### Send Friend Request

- **URL:** `/api/friend-requests/`
- **Method:** `POST`
- **Headers:**
    - `Authorization: Bearer <your-access-token>`
- **Body:**
    ```json
    {
        "to_user_id": 2
    }
    ```

### Accept/Reject Friend Request

- **URL:** `/api/friend-requests/<pk>/`
- **Method:** `PUT`
- **Headers:**
    - `Authorization: Bearer <your-access-token>`
- **Body:**
    ```json
    {
        "status": "accepted"  // or "rejected"
    }
    ```

### List Friends

- **URL:** `/api/friends/`
- **Method:** `GET`
- **Headers:**
    - `Authorization: Bearer <your-access-token>`

### List Pending Friend Requests

- **URL:** `/api/pending-requests/`
- **Method:** `GET`
- **Headers:**
    - `Authorization: Bearer <your-access-token>`

## Project Structure

```plaintext
social-network-api/
│
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── social_network/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```