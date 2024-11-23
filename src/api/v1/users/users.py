from dependency_injector.wiring import inject
from fastapi import APIRouter, status

from api.deps import CurrentUser
from schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=UserResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bad credentials",
        }
    }
)
@inject
async def get_me(user: CurrentUser):
    return user
