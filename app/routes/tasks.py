from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from models import Task, TaskCreate, PermissionEnum
from dependencies import has_permission, get_database

router = APIRouter()


@router.get(
    "/{task_id}",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.READ))],
)
async def read_task(task_id: str, db=Depends(get_database)):
    task_data = db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**task_data)


@router.post(
    "/",
    response_model=Task,
    dependencies=[Depends(has_permission(PermissionEnum.WRITE))],
)
async def create_task(task: TaskCreate, db=Depends(get_database)):
    task_dict = task.model_dump()
    result = db["tasks"].insert_one(task_dict)
    created_task = Task(**task_dict, id=result.inserted_id)

    # Update the agent tasks list
    db["agents"].update_one(
        {"_id": task.agent_id}, {"$push": {"tasks": result.inserted_id}}
    )

    return created_task


@router.delete(
    "/{task_id}",
    dependencies=[Depends(has_permission(PermissionEnum.DELETE))],
)
async def delete_task(task_id: str, db=Depends(get_database)):
    task = db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Remove the task from the agent tasks list
    db["agents"].update_one(
        {"_id": task["agent_id"]}, {"$pull": {"tasks": ObjectId(task_id)}}
    )

    # Delete the task
    db["tasks"].delete_one({"_id": ObjectId(task_id)})

    return {"message": "Task deleted successfully"}
