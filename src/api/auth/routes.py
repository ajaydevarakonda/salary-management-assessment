from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.api.dependencies import get_user_repository
from src.domain.user_repository import UserRepository
from src.use_cases.login_user import LoginUser

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Payload for login."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response containing the JWT access token."""

    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    repository: UserRepository = Depends(get_user_repository),
):
    """Authenticate a user and return a JWT token."""
    try:
        token = LoginUser(repository).execute(body.username, body.password)
        return TokenResponse(access_token=token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
