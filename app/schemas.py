from pydantic import BaseModel, EmailStr, ConfigDict

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str

    def __repr__(self):
        return f"UserResponse(id={self.id}, email={self.email}, name={self.name})"


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: UserResponse

