from zou.app import db
from zou.app.models.project import ProjectTaskTypeLink
from zou.app.models.task_type import TaskType
from zou.app.services.exception import ArgumentsException
from zou.app.services import tasks_service, projects_service

from .base import BaseModelResource, BaseModelsResource


class TaskTypesResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, TaskType)

    def check_read_permissions(self):
        return True

    def update_data(self, data):
        name = data.get("name", None)
        task_type = TaskType.get_by(name=name)
        if task_type is not None:
            raise ArgumentsException(
                "A task type with similar name already exists"
            )
        return data

    def post_creation(self, instance):
        tasks_service.clear_task_type_cache(str(instance.id))
        return instance.serialize()


class TaskTypeResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, TaskType)

    def check_read_permissions(self, instance):
        return True

    def update_data(self, data, instance_id):
        name = data.get("name", None)
        if name is not None:
            task_type = TaskType.get_by(name=name)
            if task_type is not None and instance_id != str(task_type.id):
                raise ArgumentsException(
                    "A task type with similar name already exists"
                )
        return data

    def post_update(self, instance_dict):
        tasks_service.clear_task_type_cache(instance_dict["id"])

    def post_delete(self, instance_dict):
        tasks_service.clear_task_type_cache(instance_dict["id"])
