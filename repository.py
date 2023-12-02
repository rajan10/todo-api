from model import Task


class TaskRepo:
    def create(self, title: str, description: str, due_date: str) -> Task:
        task = Task(title=title, description=description, due_date=due_date)
        task.save()
        return task

    def read_by_title(self, title: str) -> Task:
        task = Task.objects.get(title=title)
        return task

    def update_by_title(
        self, title: str, description: str, due_date: str, is_completed: bool
    ) -> Task:
        task = self.read_by_title(title=title)
        if task:
            task.description = description
            task.due_date = due_date
            task.is_completed = is_completed
            task.save()
        return task

    def delete(self, title: str) -> None:
        task = self.read_by_title(title=title)
        if task:
            task.delete()

    def update_status(self, title: str) -> Task:
        task = self.read_by_title(title=title)
        if task:
            is_completed = task.is_completed
            task.is_completed = not is_completed
            task.save()
        return task
