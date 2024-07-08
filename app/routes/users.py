from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models import User, UserCreate, PermissionEnum
from utils import hash_password
from dependencies import has_permission, get_database

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_user(user_id: str, db=Depends(get_database)):
    user_data = db["users"].find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user_data)


@router.post(
    "/",
    response_model=User,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_user(user: UserCreate, db=Depends(get_database)):
    hashed_password = hash_password(user.password)
    user_dict = user.model_dump(exclude={"password"})
    user_dict["password"] = hashed_password
    result = db["users"].insert_one(user_dict)
    created_user = User(**user_dict, id=result.inserted_id)
    return created_user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_user(user_id: str, db=Depends(get_database)):
    result = db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
