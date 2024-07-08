from fastapi import FastAPI
from utils import check_mongo_connection, ensure_admin_exists
from routes import auth, users, agents, tasks


async def lifespan(app: FastAPI):
    # startup actions
    check_mongo_connection()
    ensure_admin_exists()
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(agents.router, prefix="/agents")
app.include_router(tasks.router, prefix="/tasks")
