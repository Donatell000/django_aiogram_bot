import datetime
from typing import Optional, Dict, Any

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from tasks.models import Task, UserProfile, Category
from tasks.serializers import TaskSerializer


class TaskDetailService:
    def __init__(self, pk: int, data: Optional[Dict[str, Any]] = None) -> None:
        self.pk: int = pk
        self.data: Dict[str, Any] = data.copy() if data else {}
        self.task: Task = self._get_task()

    def _get_task(self) -> Task:
        try:
            return Task.objects.get(pk=self.pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")

    def get_task_data(self) -> Dict[str, Any]:
        return TaskSerializer(self.task).data

    def update_task(self) -> Response:
        if "user" in self.data:
            try:
                telegram_id: int = int(self.data["user"])
                user_profile: UserProfile = UserProfile.objects.get(telegram_id=telegram_id)
                self.data["user"] = user_profile.user.id
            except (UserProfile.DoesNotExist, ValueError):
                return Response({"user": ["Invalid telegram ID"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(self.task, data=self.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch_task(self) -> Response:
        if "is_done" in self.data:
            if not self.task.is_done and self.data["is_done"]:
                self.task.due_date = datetime.datetime.now()
            self.task.is_done = self.data["is_done"]
        self.task.save()
        return Response(TaskSerializer(self.task).data)

    def delete_task(self) -> Response:
        telegram_id: Optional[str] = self.data.get("user_id")
        category_id: Optional[str] = self.data.get("category_id")

        if telegram_id:
            try:
                user_profile: UserProfile = UserProfile.objects.get(telegram_id=telegram_id)
                if self.task.user != user_profile.user:
                    return Response({"error": "You do not have permission to delete this task"},
                                    status=status.HTTP_403_FORBIDDEN)
            except UserProfile.DoesNotExist:
                return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

        if category_id:
            try:
                category: Category = Category.objects.get(id=category_id)
                if self.task.category != category:
                    return Response({"error": "This task does not belong to the given category"},
                                    status=status.HTTP_403_FORBIDDEN)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        self.task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
