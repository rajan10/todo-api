from pydantic import BaseModel, Field
from datetime import datetime

from fields import PyObjectId


class TaskBaseSchema(BaseModel):
    description: str = Field(
        ..., min_length=10, description="Create/Update of the task"
    )
    due_date: datetime = Field(..., description="Create/Update of the task")
    is_completed: bool = Field(
        default=False, description="Provide the True or False for Task status"
    )


class TaskCreateSchema(TaskBaseSchema):
    # ... means compulsory field
    title: str = Field(..., description="Title of the task")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(), description="created date of the task"
    )


class TaskTitleSchema(BaseModel):
    title: str = Field(
        min_length=3,
        # pattern=r"^\d*$",
        description="title for task when read and delete api is hit",
    )


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskSchema(TaskBaseSchema):
    id: PyObjectId = Field(..., description="Id for Task")
    title: str = Field(..., min_length=3, description="title for the task")
    created_at: datetime = Field(..., description="created task date")
