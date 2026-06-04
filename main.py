from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# Временное хранилище вместо базы данных

class TaskEnum(str, Enum):
    TODO = "todo"
    DONE = "done"
    IN_PROGRESS = "in_progress"

class Task(BaseModel):
    id: str
    title: str
    status: TaskEnum | None = None

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    status: TaskEnum | None = None


tasks: list[Task] = []


@app.get("/tasks")
def get_tasks(status: TaskEnum | None = None) -> list[Task]:
    if status is None:
        return tasks
    else:
        return [task for task in tasks if task.status == status]



@app.post("/tasks")
def create_task(payload: TaskCreate) -> Task:
    new_task = Task(id=str(uuid4()), title=payload.title,)

    tasks.append(new_task)
    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = next((task for task in tasks if task.id == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}")
def put_task(task_id: str, payload: TaskUpdate):
    task = next((task for task in tasks if task.id == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.title:
        task.title = payload.title
    if payload.status:
        task.status = payload.status
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    task = next((task for task in tasks if task.id == task_id), None)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return task
