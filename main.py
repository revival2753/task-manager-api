from uuid import uuid4
from fastapi import FastAPI, HTTPException
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskEnum

app = FastAPI()

tasks: list[TaskResponse] = []

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(status: TaskEnum | None = None):
    if status is None:
        return tasks
    return [task for task in tasks if task.status == status]

@app.post("/tasks", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    task = TaskResponse(id=str(uuid4()), title=payload.title, status=TaskEnum.TODO)
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, payload: TaskUpdate):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title:
        task.title = payload.title
    if payload.status:
        task.status = payload.status
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return {"detail": "Task deleted"}