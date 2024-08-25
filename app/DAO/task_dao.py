from bson import ObjectId


class TaskDAO:
    def __init__(self, db):
        self.collection = db["tasks"]

    def find_task_by_id(self, task_id: str):
        return self.collection.find_one({"_id": ObjectId(task_id)})

    def insert_task(self, task_dict: dict):
        return self.collection.insert_one(task_dict)

    def delete_task_by_id(self, task_id: str):
        return self.collection.delete_one({"_id": ObjectId(task_id)})
