from bson import ObjectId
from fastapi import HTTPException
from DAO.task_dao import TaskDAO
from DAO.agent_dao import AgentDAO
from models import Task, TaskCreate


class TaskController:
    def __init__(self, task_dao: TaskDAO, agent_dao: AgentDAO):
        self.task_dao = task_dao
        self.agent_dao = agent_dao

    async def read_task(self, task_id: str):
        task_data = self.task_dao.find_task_by_id(task_id)
        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**task_data)

    async def create_task(self, task: TaskCreate):
        task_dict = task.model_dump()
        result = self.task_dao.insert_task(task_dict)
        created_task = Task(**task_dict, id=result.inserted_id)

        # Atualizar a lista de tarefas do agente
        self.agent_dao.add_task_to_agent(task.agent_id, result.inserted_id)

        return created_task

    async def delete_task(self, task_id: str):
        task = self.task_dao.find_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Remover tarefa da lista de tarefas do agente
        self.agent_dao.remove_task_from_agent(task["agent_id"], ObjectId(task_id))

        # Deletar tarefa
        self.task_dao.delete_task_by_id(task_id)

        return {"message": "Task deleted successfully"}
