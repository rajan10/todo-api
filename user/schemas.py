from pydantic import BaseModel, Field


# User schemea
class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=4, description="username of the User")
    password: str = Field(..., min_length=4, description="password of the User")


class UserReadSchema(BaseModel):
    username: str = Field(..., description="username for User when read api is hit")


class UserUpdateSchema(BaseModel):
    username: str = Field(..., description="Update of the Username")
    password: str = Field(..., min_length=5, description="Update of the Password")


class UserDeleteSchema(BaseModel):
    username: str = Field(..., description="deletion of the username")
