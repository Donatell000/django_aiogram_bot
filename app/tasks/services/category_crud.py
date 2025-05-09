from typing import Optional

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from tasks.models import Category, UserProfile
from tasks.serializers import CategorySerializer


class CategoryCrudService:
    def __init__(self) -> None:
        self.user: Optional[User] = None

    def _get_user_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            return user_profile.user
        except UserProfile.DoesNotExist:
            return None

    def _get_or_create_user_by_telegram_id(self, telegram_id: str) -> User:
        user = self._get_user_by_telegram_id(telegram_id)
        if user:
            return user

        user = User.objects.create(username=f"user_{telegram_id}")
        UserProfile.objects.create(user=user, telegram_id=telegram_id)
        return user

    def handle_category_get(self, request) -> Response:
        telegram_id = request.query_params.get("user_id")
        if not telegram_id:
            return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

        self.user = self._get_or_create_user_by_telegram_id(telegram_id)
        categories = Category.objects.filter(user=self.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def handle_category_post(self, request) -> Response:
        telegram_id = request.data.get("user_id")
        if not telegram_id:
            return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

        self.user = self._get_or_create_user_by_telegram_id(telegram_id)
        data = request.data.copy()
        data["user"] = self.user.id

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
