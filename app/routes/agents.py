from fastapi import APIRouter, Depends
from models import AgentBase, PermissionEnum, User, Agent
from dependencies import has_permission, get_database, get_current_user
from controllers.agent_controller import AgentController
from DAO.agent_dao import AgentDAO

router = APIRouter()


@router.get(
    "/{agent_id}",
    response_model=Agent,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_agent(agent_id: str, db=Depends(get_database)):
    agent_dao = AgentDAO(db)
    agent_controller = AgentController(agent_dao)
    return await agent_controller.read_agent(agent_id)


@router.post(
    "/",
    response_model=Agent,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_agent(
    agent_data: AgentBase,
    current_user: User = Depends(get_current_user),
    db=Depends(get_database),
):
    agent_dao = AgentDAO(db)
    agent_controller = AgentController(agent_dao)
    return await agent_controller.create_agent(agent_data, current_user)


@router.delete(
    "/{agent_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_agent(agent_id: str, db=Depends(get_database)):
    agent_dao = AgentDAO(db)
    agent_controller = AgentController(agent_dao)
    return await agent_controller.delete_agent(agent_id)
