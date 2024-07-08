from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Token
from utils import create_access_token, verify_password
from database import get_database

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)
):
    user = db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": str(user["_id"])})
    return Token(access_token=access_token, token_type="bearer")
