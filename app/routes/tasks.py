from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models import Task, TaskCreate, PermissionEnum
from controllers.task_controller import TaskController
from dependencies import has_permission, get_database


router = APIRouter()


@router.get(
    "/{task_id}",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_task(task_id: str, db=Depends(get_database)):
    task_controller = TaskController(db=db)
    return await task_controller.read_task(task_id)


@router.post(
    "/",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_task(task: TaskCreate, db=Depends(get_database)):
    task_controller = TaskController(db=db)
    return await task_controller.create_task(task)


@router.delete(
    "/{task_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_task(task_id: str, db=Depends(get_database)):
    task_controller = TaskController(db=db)
    return await task_controller.delete_task(task_id)
