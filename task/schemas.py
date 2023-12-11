from pydantic import BaseModel, Field
from datetime import datetime


class TaskSchema(BaseModel):
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
