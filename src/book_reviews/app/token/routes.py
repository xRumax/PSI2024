from fastapi import APIRouter
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .services import TokenService
from .schemas import TokenIn
from fastapi import HTTPException, status

router = APIRouter()


@router.post("/token")
@inject
async def login_for_access_token(
    form_data: TokenIn,
    token_service: TokenService = Depends(Provide[Container.token_service]),
):
    user = token_service.login(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = token_service.login(form_data)
    return {"access_token": access_token, "token_type": "bearer"}
