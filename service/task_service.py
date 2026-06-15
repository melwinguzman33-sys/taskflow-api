from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model.task_model import Task
from model.user_model import User
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db=db)

    def create_task(self, task_data: TaskCreate, current_user: User) -> Task:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status="pending",
            owner_id=current_user.id,
        )
        return self.task_repository.create(new_task)

    def get_my_tasks(self, current_user: User) -> list[Task]:
        return self.task_repository.get_all_by_owner(current_user.id)

    def get_task_by_id(self, task_id: int, current_user: User) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La tarea no fue encontrada",
            )

        if task.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta acción",
            )

        return task

    def update_task(self, task_id: int, task_data: TaskUpdate, current_user: User) -> Task:
        task = self.get_task_by_id(task_id, current_user)

        if task_data.status is not None:
            self._validate_status_transition(task.status, task_data.status)
            task.status = task_data.status

        if task_data.title is not None:
            task.title = task_data.title

        if task_data.description is not None:
            task.description = task_data.description

        if task_data.priority is not None:
            task.priority = task_data.priority

        return self.task_repository.update(task)

    def delete_task(self, task_id: int, current_user: User) -> None:
        task = self.get_task_by_id(task_id, current_user)
        self.task_repository.delete(task)

    def _validate_status_transition(self, current_status: str, new_status: str) -> None:
        valid_statuses = ["pending", "in_progress", "done"]

        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado inválido. Debe ser: pending, in_progress o done",
            )

        if current_status == "pending" and new_status == "done":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una tarea no puede pasar de 'pendiente' a 'completada' directamente. Debe pasar primero por 'en progreso'",
            )