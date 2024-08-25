from fastapi import HTTPException
from models import Agent, AgentBase, User
from DAO.agent_dao import AgentDAO


class AgentController:
    def __init__(self, agent_dao: AgentDAO):
        self.agent_dao = agent_dao

    async def read_agent(self, agent_id: str):
        agent_data = self.agent_dao.find_agent_by_id(agent_id)
        if not agent_data:
            raise HTTPException(status_code=404, detail="Agent not found")
        return Agent(**agent_data)

    async def create_agent(self, agent_data: AgentBase, current_user: User):
        agent_dict = agent_data.model_dump()
        agent_dict["user_id"] = current_user.id
        result = self.agent_dao.insert_agent(agent_dict)
        created_agent = Agent(**agent_dict, id=result.inserted_id)
        return created_agent

    async def delete_agent(self, agent_id: str):
        result = self.agent_dao.delete_agent_by_id(agent_id)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent deleted successfully"}
