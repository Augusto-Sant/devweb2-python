import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import json
from dotenv import load_dotenv
from typing import Optional
from pymongo import MongoClient
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_database = os.getenv("MONGO_INITDB_DATABASE")


class User(BaseModel):
    id: Optional[int] = None
    name: str
    age: int


def get_mongo_client():
    client = MongoClient(
        f"mongodb://{mongo_username}:{mongo_password}@mongodb:27017/{mongo_database}?authSource=admin"
    )
    try:
        yield client
    finally:
        client.close()


def get_database(client: MongoClient = Depends(get_mongo_client)):
    return client[mongo_database]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup commands
    try:
        # Check MongoDB connection
        mongo_client = MongoClient(
            f"mongodb://{mongo_username}:{mongo_password}@mongodb:27017/{mongo_database}?authSource=admin"
        )
        mongo_client.admin.command("ping")
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise e

    yield
    # shutdown commands


app = FastAPI(lifespan=lifespan)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db=Depends(get_database)):
    user_data = db["users"].find_one({"id": user_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user_data)


@app.post("/users/", response_model=User)
async def create_user(user: User, db=Depends(get_database)):
    user_id = db["users"].count_documents({}) + 1
    user.id = user_id
    db["users"].insert_one(user.dict())
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db=Depends(get_database)):
    result = db["users"].delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
