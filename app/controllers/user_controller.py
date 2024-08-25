from fastapi import HTTPException
from bson import ObjectId
from models import User, UserCreate
from utils import hash_password


class UserController:
    def __init__(self, db):
        self.db = db

    async def read_user(self, user_id: str):
        user_data = self.db["users"].find_one({"_id": ObjectId(user_id)})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user_data)

    async def create_user(self, user: UserCreate):
        hashed_password = hash_password(user.password)
        user_dict = user.model_dump(exclude={"password"})
        user_dict["password"] = hashed_password
        result = self.db["users"].insert_one(user_dict)
        created_user = User(**user_dict, id=result.inserted_id)
        return created_user

    async def delete_user(self, user_id: str):
        result = self.db["users"].delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
