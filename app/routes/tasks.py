from fastapi import APIRouter, Depends
from models import Task, TaskCreate, PermissionEnum
from controllers.task_controller import TaskController
from DAO.task_dao import TaskDAO
from DAO.agent_dao import AgentDAO
from dependencies import has_permission, get_database


router = APIRouter()


@router.get(
    "/{task_id}",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_task(task_id: str, db=Depends(get_database)):
    task_dao = TaskDAO(db)
    agent_dao = AgentDAO(db)
    task_controller = TaskController(task_dao=task_dao, agent_dao=agent_dao)
    return await task_controller.read_task(task_id)


@router.post(
    "/",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_task(task: TaskCreate, db=Depends(get_database)):
    task_dao = TaskDAO(db)
    agent_dao = AgentDAO(db)
    task_controller = TaskController(task_dao=task_dao, agent_dao=agent_dao)
    return await task_controller.create_task(task)


@router.delete(
    "/{task_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_task(task_id: str, db=Depends(get_database)):
    task_dao = TaskDAO(db)
    agent_dao = AgentDAO(db)
    task_controller = TaskController(task_dao=task_dao, agent_dao=agent_dao)
    return await task_controller.delete_task(task_id)


@router.get(
    "/agent/{agent_id}/tasks",
    response_model=list[Task],
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def list_tasks_by_agent(agent_id: str, db=Depends(get_database)):
    task_dao = TaskDAO(db)
    agent_dao = AgentDAO(db)
    task_controller = TaskController(task_dao=task_dao, agent_dao=agent_dao)
    return await task_controller.list_tasks_by_agent(agent_id)
