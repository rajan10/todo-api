from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreateSchema(BaseModel):
    # ... means compulsory field
    title: str = Field(..., description="Title of the task")
    description: str = Field(..., description="descripton of the task")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(), description="created date of the task"
    )
    due_date: datetime = Field(..., description="due date of the task")
    is_completed: bool = Field(
        default=False, description="boolean value of the Task by defalut it is False"
    )


class TaskReadSchema(BaseModel):
    title: str = Field(
        min_length=3,
        # pattern=r"^\d*$",
        description="title for task when read api is hit",
    )


class TaskUpdateSchema(BaseModel):
    description: str = Field(..., min_length=10, description="Update of the task")
    due_date: datetime = Field(..., description="Update of the task")
    is_completed: bool = Field(..., description="Provide the True or False Task status")


class TaskDeleteSchema(BaseModel):
    title: str = Field(..., max_length=100, description="Delete the task")
