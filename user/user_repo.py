from user.model import User


class UserRepo:
    def create(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        user.save()
        return user

    def read_by_username(self, username: str) -> User:
        user = User.objects.get(username=username)
        if user:
            return user

    def read_all(self) -> list[str]:
        users = User.objects()
        if users:
            return users
        return []

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
