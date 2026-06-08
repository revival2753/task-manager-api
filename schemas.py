from pydantic import BaseModel
from enum import Enum

class TaskEnum(str, Enum):
    TODO = "todo"
    DONE = "done"
    IN_PROGRESS = "in_progress"

class TaskResponse(BaseModel):
    id: str
    title: str
    status: TaskEnum

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    status: TaskEnum | None = None