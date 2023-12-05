from model import Task, User


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


class UserRepo:
    def create(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        user.save()
        return user

    def read_by_username(self, username: str) -> User:
        user = User.objects.get(username=username)
        if user:
            return user

    def update_by_username(self, username: str, password: str) -> User:
        user = self.read_by_username(username=username)
        if user:
            user.password = password
        user.save()
        return user

    def delete_by_username(self, username: str) -> None:
        user = self.read_by_username(username=username)
        if user:
            user.delete()
