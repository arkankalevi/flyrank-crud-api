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

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- Docker
- Uvicorn
- Pydantic
- Psycopg
- python-dotenv

## Requirements

- Python 3.10+
- Git
- Docker Desktop

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
   ```
   
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
uvicorn main:app --reload
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

Swagger UI can be used to test all CRUD endpoints.

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

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns basic API information |
| GET | `/health` | Checks API health |
| GET | `/tasks` | Returns all tasks |
| GET | `/tasks/{id}` | Returns one task |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/{id}` | Updates an existing task |
| DELETE | `/tasks/{id}` | Deletes a task |


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

The existing API routes continue to use the same database function interface.

The storage implementation was changed from SQLite to PostgreSQL without changing the API routes in `main.py`.

The architecture is:

```text
Client
   ↓
FastAPI routes
   ↓
database.py
   ↓
Psycopg
   ↓
PostgreSQL
   ↓
Docker volume: taskdata
```

This demonstrates that the storage implementation can be switched without changing the API routes.