from fastapi import APIRouter, Depends
from models import User, UserCreate, PermissionEnum
from controllers.user_controller import UserController
from dependencies import has_permission, get_database


router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_user(user_id: str, db=Depends(get_database)):
    user_controller = UserController(db=db)
    return await user_controller.read_user(user_id)


@router.post(
    "/",
    response_model=User,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_user(user: UserCreate, db=Depends(get_database)):
    user_controller = UserController(db=db)
    return await user_controller.create_user(user)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_user(user_id: str, db=Depends(get_database)):
    user_controller = UserController(db=db)
    return await user_controller.delete_user(user_id)
