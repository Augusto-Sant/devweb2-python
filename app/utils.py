import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from pymongo import MongoClient
import bcrypt
import jwt

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE = os.getenv("MONGO_INITDB_DATABASE")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

MONGO_CONNECTION_URL = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    + f"@mongodb:27017/{MONGO_DATABASE}?authSource=admin"
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def check_mongo_connection():
    try:
        mongo_client = MongoClient(MONGO_CONNECTION_URL)
        mongo_client.admin.command("ping")
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise e


def ensure_admin_exists():
    mongo_client = MongoClient(MONGO_CONNECTION_URL)
    db = mongo_client[MONGO_DATABASE]
    existing_admin = db["users"].find_one({"username": ADMIN_USERNAME})
    if not existing_admin:
        admin_user = dict(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            # should have all permissions
            permissions=["read", "write", "delete"],
        )
        hashed_password = hash_password(admin_user["password"])
        admin_user["password"] = hashed_password
        db["users"].insert_one(admin_user)
        print(f"Admin user {ADMIN_USERNAME} created successfully.")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
