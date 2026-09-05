import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client, Client

from database import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)

from auth import AuthRequest
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

security = HTTPBearer(auto_error=False)

def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "Access token required"}
        )

    return credentials.credentials

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PORT = int(os.getenv("PORT", "8000"))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in .env"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()



tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Read FlyRank assignment", "done": True},
]


@app.get("/", description="Returns basic information about the Task API.")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", description="Checks whether the API server is running.")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", description="Returns all tasks.")
def get_tasks():
    return get_all_tasks()

@app.get("/tasks/{id}", description="Returns one task by its ID.")
def get_task(id: int):
    task = get_task_by_id(id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return task

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.post("/tasks", status_code=201, description="Creates a new task.")
def create_task_endpoint(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required and cannot be empty"}
        )

    return create_task(task.title)

@app.put("/tasks/{id}", description="Updates an existing task.")
def update_task_endpoint(id: int, task_update: TaskUpdate):

    if task_update.title is None and task_update.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "at least one field is required"}
        )

    if task_update.title is not None:
        if not task_update.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "title cannot be empty"}
            )

    updated_task = update_task(
        id,
        task_update.title,
        task_update.done
    )

    if updated_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return updated_task
@app.delete(
    "/tasks/{id}",
    status_code=204,
    description="Deletes a task by its ID."
)
def delete_task_endpoint(id: int):

    deleted = delete_task(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(auth_request: AuthRequest):
    if not auth_request.email or not auth_request.password:
        raise HTTPException(
            status_code=400,
            detail={"error": "Email and password are required"}
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": auth_request.email,
                "password": auth_request.password,
            }
        )

        return {
            "user": response.user
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail={"error": "Signup failed"}
        )

@app.post("/auth/login")
def login(auth_request: AuthRequest):
    if not auth_request.email or not auth_request.password:
        raise HTTPException(
            status_code=400,
            detail={"error": "Email and password are required"}
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": auth_request.email,
                "password": auth_request.password,
            }
        )

        if not response.session:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid login credentials"}
            )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid login credentials"}
        )

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }

@app.get("/protected/profile")
def protected_profile(token: str = Depends(get_token)):
    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if user is None:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid or expired token"}
            )

        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid or expired token"}
        )
    
if __name__ == "__main__":
    import uvicorn

    print("Server running and connected to Supabase")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
    )

