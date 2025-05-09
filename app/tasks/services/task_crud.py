from typing import Dict, Any, Tuple

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from rest_framework import status

from tasks.models import Task, Category, UserProfile
from tasks.serializers import TaskSerializer


class TaskCrudService:
    def __init__(self, request: Any) -> None:
        self.request = request
        self.telegram_id = self.request.query_params.get("user_id") if self.request.method == "GET" else self.request.data.get("user_id")
        self.category_id = self.request.query_params.get("category_id") if self.request.method == "GET" else self.request.data.get("category_id")
        self.user: User | None = None
        self.category: Category | None = None

        if not self.telegram_id:
            raise ValueError("user_id is required")

        self.telegram_id = str(self.telegram_id)

    def _get_or_create_user(self) -> None:
        try:
            user_profile = UserProfile.objects.get(telegram_id=self.telegram_id)
            self.user = user_profile.user
        except UserProfile.DoesNotExist:
            self.user = User.objects.create(username=f"user_{self.telegram_id}")
            UserProfile.objects.create(user=self.user, telegram_id=self.telegram_id)

    def _get_category(self) -> None:
        if self.category_id:
            try:
                self.category = Category.objects.get(id=self.category_id)
            except Category.DoesNotExist:
                raise NotFound("Category not found")

    def _get_tasks(self) -> Any:
        tasks = Task.objects.filter(user=self.user)
        if self.category:
            tasks = tasks.filter(category=self.category)
        return tasks

    def _create_task(self, task_data: Dict[str, Any]) -> Task:
        task_data["user"] = self.user.id
        task_data["category_id"] = self.category.id
        serializer = TaskSerializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def handle_get(self) -> Tuple[Dict[str, Any], int]:
        if not self.telegram_id:
            return {"error": "user_id required"}, status.HTTP_400_BAD_REQUEST

        self._get_or_create_user()

        try:
            self._get_category()
        except NotFound as e:
            return {"error": str(e)}, status.HTTP_404_NOT_FOUND

        tasks = self._get_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data, status.HTTP_200_OK

    def handle_post(self) -> Tuple[Dict[str, Any], int]:
        if not self.telegram_id or not self.category_id:
            return {"error": "user_id and category_id required"}, status.HTTP_400_BAD_REQUEST

        self._get_or_create_user()

        try:
            self._get_category()
        except NotFound as e:
            return {"error": str(e)}, status.HTTP_404_NOT_FOUND

        try:
            task = self._create_task(self.request.data.copy())
            serializer = TaskSerializer(task)
            return serializer.data, status.HTTP_201_CREATED
        except NotFound as e:
            return {"error": str(e)}, status.HTTP_404_NOT_FOUND
