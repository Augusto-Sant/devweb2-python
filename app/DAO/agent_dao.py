from bson import ObjectId


class AgentDAO:
    def __init__(self, db):
        self.collection = db["agents"]

    def add_task_to_agent(self, agent_id: str, task_id: ObjectId):
        self.collection.update_one({"_id": agent_id}, {"$push": {"tasks": task_id}})

    def remove_task_from_agent(self, agent_id: str, task_id: ObjectId):
        self.collection.update_one({"_id": agent_id}, {"$pull": {"tasks": task_id}})
