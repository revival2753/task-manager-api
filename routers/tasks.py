from fastapi import APIRouter, HTTPException
from uuid import uuid4
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskEnum

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[TaskResponse] = []

@router.get("", response_model=list[TaskResponse])
def get_tasks(status: TaskEnum | None = None):
    if status is None:
        return tasks
    return [task for task in tasks if task.status == status]

@router.post("", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    task = TaskResponse(id=str(uuid4()), title=payload.title, tags=payload.tags, status=TaskEnum.TODO)
    tasks.append(task)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, payload: TaskUpdate):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title:
        task.title = payload.title
    if payload.tags:
        task.tags = payload.tags
    if payload.status:
        task.status = payload.status
    return task

@router.delete("/{task_id}")
def delete_task(task_id: str):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return {"detail": "Task deleted"}