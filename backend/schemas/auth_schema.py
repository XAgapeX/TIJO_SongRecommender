from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(BaseModel):
    email: str = Field(max_length=254)
    username: str | None = Field(default=None, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    password_confirm: str = Field(min_length=8, max_length=128)
    terms_accepted: bool
    marketing_consent: bool = False
    website: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str | None = None
    email: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


class RegistrationResponse(BaseModel):
    message: str
    verification_url: str | None = None


class FavoriteRequest(BaseModel):
    track_id: str
