"""Requirement
   1. create a db collection name Task with required fields for todo-application
   2. Create  a repository for it
   3. Create a POST request to create a task through API 
   4. Send the created data as response of  API call
   """
from utils import get_current_date
from mongoengine import Document, StringField, DateTimeField, BooleanField


class Task(Document):
    title = StringField(max_length=100, required=True)
    description = StringField(max_length=300, required=True)
    created_at = DateTimeField(default=get_current_date)
    due_date = DateTimeField(required=True)
    is_completed = BooleanField(default=False)

    def __str__(self):
        return f"<Task> {self.name}>"
