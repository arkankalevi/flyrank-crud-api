# FlyRank W3 A1 — Connecting CRUD API to PostgreSQL

A CRUD API built with Python and FastAPI as part of the FlyRank AI Internship W3 A1 assignment.

The API manages a to-do task list using PostgreSQL running in Docker for persistent storage.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- 400 error handling
- 404 error handling
- Swagger UI documentation
- PostgreSQL database storage
- Dockerized PostgreSQL
- Persistent data across container and server restarts
- User signup
- User login
- JWT authentication
- Protected endpoint
- Public endpoint
- User logout
- Reusable JWT authentication dependency

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- Docker
- Supabase
- Uvicorn
- Pydantic
- Psycopg
- python-dotenv
- JWT

## Requirements

- Python 3.10+
- Git
- Docker Desktop
- Supabase project

## Installation

Clone the repository:

```bash
git clone https://github.com/arkankalevi/flyrank-crud-api

cd flyrank-crud-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
PORT=8000
```

Use `.env.example` as a template.

Do not commit the `.env` file to Git because it contains environment-specific configuration and credentials.

## Running the API

### 1. Start PostgreSQL

Make sure Docker Desktop is running.

Start the PostgreSQL container:

```powershell
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:17
```

Check that the PostgreSQL container is running:

```powershell
docker ps
```

The container should appear with the name:

```text
taskdb
```

### 2. Start the FastAPI server

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Start the FastAPI server:

```powershell
python main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 3. Open Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all CRUD and authentication endpoints.

### 4. Stop the API

To stop the FastAPI server, press:

```text
CTRL + C
```

### 5. Stop PostgreSQL

To stop the PostgreSQL container:

```powershell
docker stop taskdb
```

To start the existing PostgreSQL container again:

```powershell
docker start taskdb
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/` | Returns basic API information | No |
| GET | `/health` | Checks API health | No |
| GET | `/tasks` | Returns all tasks | No |
| GET | `/tasks/{id}` | Returns one task | No |
| POST | `/tasks` | Creates a new task | No |
| PUT | `/tasks/{id}` | Updates an existing task | No |
| DELETE | `/tasks/{id}` | Deletes a task | No |
| POST | `/auth/signup` | Creates a new user account | No |
| POST | `/auth/login` | Authenticates an existing user | No |
| POST | `/auth/logout` | Logs out the current user | Yes |
| GET | `/public/info` | Returns public information | No |
| GET | `/protected/profile` | Returns the authenticated user's profile | Yes |


## Swagger UI

The API provides interactive Swagger UI documentation for testing and exploring the available API endpoints.

The Swagger UI can be accessed locally at:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface for testing the CRUD API and authentication endpoints.

### Swagger UI - API Documentation

The following screenshot shows the available API endpoints in Swagger UI, including CRUD operations and authentication endpoints.

![Swagger UI - API Documentation](swagger1.png.png)

### Swagger UI - Authentication

The following screenshot shows the authentication-related endpoints, including signup, login, logout, public information, and the protected profile endpoint.

![Swagger UI - Authentication](swagger2.png.png)

### Using Swagger UI

To test the protected endpoint:

1. Start the FastAPI server.
2. Open `http://127.0.0.1:8000/docs`.
3. Use `POST /auth/login` with a registered account.
4. Copy the `access_token` returned by the login endpoint.
5. Click the `Authorize` button in Swagger UI.
6. Enter the access token.
7. Click `Authorize`.
8. Open `GET /protected/profile`.
9. Click `Try it out`.
10. Click `Execute`.

A valid access token should return:

```text
200 OK
```

Accessing the protected endpoint without a valid token should return:

```text
401 Unauthorized
```

The public endpoint can be accessed without authentication.

The Swagger UI documentation allows a peer to understand and test the API without needing to inspect the source code.
## Authentication

The API uses Supabase Authentication with JWT access tokens.

Authentication logic is separated into `auth.py` to provide reusable authentication functionality.

### Signup

Creates a new user account.

**Endpoint:**

```text
POST /auth/signup
```

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Successful response:**

```text
201 Created
```

### Login

Authenticates an existing user.

**Endpoint:**

```text
POST /auth/login
```

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Successful response:**

```text
200 OK
```

The response contains authentication tokens:

```json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>"
}
```

The `access_token` is used to access protected endpoints.

### Protected Profile

**Endpoint:**

```text
GET /protected/profile
```

This endpoint requires a valid JWT access token.

The request must include:

```text
Authorization: Bearer <access_token>
```

**Successful response:**

```text
200 OK
```

Example:

```json
{
  "id": "<user_id>",
  "email": "user@example.com",
  "created_at": "<timestamp>"
}
```

Without a token:

```text
401 Unauthorized
```

An invalid or expired token also results in:

```text
401 Unauthorized
```

### Public Info

**Endpoint:**

```text
GET /public/info
```

This endpoint does not require authentication.

**Successful response:**

```text
200 OK
```

Example:

```json
{
  "message": "Welcome stranger! This info is public."
}
```

### Logout

**Endpoint:**

```text
POST /auth/logout
```

This endpoint logs the current user out through Supabase Authentication.

**Successful response:**

```text
200 OK
```

Example:

```json
{
  "message": "Logout successful"
}
```

## Swagger Bearer Authentication

Swagger UI provides an `Authorize` button for testing protected endpoints.

To test `/protected/profile`:

1. Login using `POST /auth/login`.
2. Copy the returned `access_token`.
3. Click `Authorize` in Swagger UI.
4. Enter the access token.
5. Click `Authorize`.
6. Call `GET /protected/profile`.
7. The request should return `200 OK`.

The authorization header is sent as:

```text
Authorization: Bearer <access_token>
```

Do not include a real access token in this README or commit it to Git.

## Authentication Testing

The authentication flow was tested using the following cases:

| Test | Expected Result |
|---|---|
| Signup with valid credentials | `201 Created` |
| Login with valid credentials | `200 OK` |
| Login with incorrect password | `401 Unauthorized` |
| Signup with empty fields | `400 Bad Request` |
| Access protected route without token | `401 Unauthorized` |
| Access protected route with valid token | `200 OK` |
| Access protected route with invalid token | `401 Unauthorized` |
| Access public route without token | `200 OK` |
| Logout | `200 OK` |

## PostgreSQL Database

The application uses PostgreSQL as its persistent database.

PostgreSQL runs inside a Docker container named `taskdb`.

The application connects to PostgreSQL using the `DATABASE_URL` environment variable from `.env`.

The PostgreSQL database is named `tasks`.

The database connection is handled in `database.py` using `psycopg`.

## Database Schema

The database contains a table named `tasks`.

| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| title | TEXT | Task title |
| done | BOOLEAN | Completion status |

The table is automatically created when the application starts if it does not already exist.

The SQL structure is:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
```

## Persistence

The PostgreSQL database uses a Docker volume named `taskdata` to persist data.

Persistence was tested by creating a task through the API:

```text
Persistence Test
```

The task was verified in PostgreSQL using:

```powershell
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

The PostgreSQL container was then restarted:

```powershell
docker restart taskdb
```

After the restart, the task was still present in the database.

The API was also restarted, and `GET /tasks` still returned the `Persistence Test` task.

This proves that the data persists across a PostgreSQL container restart because the database uses the `taskdata` Docker volume.

## Repository Architecture

The PostgreSQL repository implementation is contained in `database.py`.

The authentication logic and reusable JWT verification are contained in `auth.py`.

The existing API routes continue to use the same database function interface.

The storage implementation was changed from SQLite to PostgreSQL without changing the API routes in `main.py`.

The architecture is:

```text
Client
   ↓
FastAPI routes
   ↓
   ├── Authentication routes
   │       ↓
   │    auth.py
   │       ↓
   │    Supabase Auth
   │
   └── CRUD routes
           ↓
       database.py
           ↓
         Psycopg
           ↓
       PostgreSQL
           ↓
       Docker volume: taskdata

## Error Handling

The API returns appropriate HTTP status codes for common errors.

### 400 Bad Request

Used when request data is invalid or required authentication input is missing.

### 401 Unauthorized

Used when authentication credentials are missing, invalid, or expired.

### 404 Not Found

Used when a requested task does not exist.

## Security Notes

- `.env` must not be committed to Git.
- Real Supabase credentials must not be placed in `.env.example`.
- Real access tokens and refresh tokens must not be placed in source code or documentation.
- Protected endpoints require a valid JWT access token.
- Authentication is handled through Supabase Authentication.