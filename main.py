import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(BaseModel):
    id: int
    name: str
    email: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup commands
    yield
    # shutdown commands


app = FastAPI(lifespan=lifespan)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):

    user_data = redis_client.get(f"user:{user_id}")

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    user = json.loads(user_data)
    return user


@app.post("/users/", response_model=User)
async def create_user(user: User):

    if not redis_client.exists("user_counter"):
        redis_client.set("user_counter", 0)
    user.id = redis_client.incr("user_counter")

    user_data = json.dumps(user.model_dump())
    redis_client.set(f"user:{user.id}", user_data)
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    result = redis_client.delete(f"user:{user_id}")

    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
