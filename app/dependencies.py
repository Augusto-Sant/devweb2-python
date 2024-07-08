from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from models import User, PermissionEnum
from utils import decode_token
from database import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db=Depends(get_database)
):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)


def has_permission(required_permission: PermissionEnum):
    def check_permission(current_user: User = Depends(get_current_user)):
        if required_permission not in current_user.permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user

    return check_permission
