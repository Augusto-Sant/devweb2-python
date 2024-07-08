from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models import Agent, AgentBase, PermissionEnum, User
from dependencies import has_permission, get_database, get_current_user

router = APIRouter()


@router.get(
    "/{agent_id}",
    response_model=Agent,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_agent(agent_id: str, db=Depends(get_database)):
    agent_data = db["agents"].find_one({"_id": ObjectId(agent_id)})
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    return Agent(**agent_data)


@router.post(
    "/",
    response_model=Agent,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_agent(
    agent_data: AgentBase,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    agent_dict = agent_data.model_dump()
    agent_dict["user_id"] = current_user.id
    result = db["agents"].insert_one(agent_dict)
    created_agent = Agent(**agent_dict, id=result.inserted_id)
    return created_agent


@router.delete(
    "/{agent_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_agent(agent_id: str, db=Depends(get_database)):
    result = db["agents"].delete_one({"_id": ObjectId(agent_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}
