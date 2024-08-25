from bson import ObjectId


class AgentDAO:
    def __init__(self, db):
        self.collection = db["agents"]

    def add_task_to_agent(self, agent_id: str, task_id: ObjectId):
        self.collection.update_one({"_id": agent_id}, {"$push": {"tasks": task_id}})

    def remove_task_from_agent(self, agent_id: str, task_id: ObjectId):
        self.collection.update_one({"_id": agent_id}, {"$pull": {"tasks": task_id}})

    def find_agent_by_id(self, agent_id: str):
        return self.collection.find_one({"_id": ObjectId(agent_id)})

    def insert_agent(self, agent_dict: dict):
        return self.collection.insert_one(agent_dict)

    def delete_agent_by_id(self, agent_id: str):
        return self.collection.delete_one({"_id": ObjectId(agent_id)})

    def find_tasks_by_agent(self, agent_id: str):
        agent = self.find_agent_by_id(agent_id)
        if not agent or "tasks" not in agent:
            return []
        return list(self.tasks_collection.find({"_id": {"$in": agent["tasks"]}}))
