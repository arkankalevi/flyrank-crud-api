from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import initialize_database, get_all_tasks, get_task_by_id, create_task

app = FastAPI()

initialize_database()

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
def update_task(id: int, task_update: TaskUpdate):

    if task_update.title is None and task_update.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "at least one field is required"}
        )

    for task in tasks:
        if task["id"] == id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "title cannot be empty"}
                    )
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}", status_code=204, description="Deletes a task by its ID.")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )