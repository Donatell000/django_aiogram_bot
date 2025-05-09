from typing import Optional, Dict

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from tasks.models import Category, UserProfile
from tasks.serializers import CategorySerializer


class CategoryDetailService:
    def __init__(self, request) -> None:
        self.request = request
        self.telegram_id = self._get_telegram_id()
        self.user = self._get_user_by_telegram_id()

    def _get_telegram_id(self) -> str:
        if self.request.method == 'GET':
            telegram_id = self.request.query_params.get("user_id")
        else:
            telegram_id = self.request.data.get("user_id")

        if not telegram_id:
            raise ValueError("user_id required")

        return telegram_id

    def _get_user_by_telegram_id(self) -> UserProfile:
        try:
            return UserProfile.objects.get(telegram_id=self.telegram_id).user
        except UserProfile.DoesNotExist:
            raise Http404("Пользователь не найден")

    def get(self, pk: int) -> Response:
        try:
            category = self._get_category(pk)
            data = self._serialize_category(category)
            return Response(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, pk: int) -> Response:
        try:
            category = self._get_category(pk)

            data = self.request.data.copy()
            data["user"] = self.user.id

            updated_data = self._update_category(category, data)
            if updated_data:
                return Response(updated_data)

            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, pk: int) -> Response:
        try:
            category = self._get_category(pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def _get_category(self, pk: int) -> Category:
        try:
            return Category.objects.get(pk=pk, user=self.user)
        except Category.DoesNotExist:
            raise Http404("Категория не найдена")

    def _serialize_category(self, category: Category) -> Dict:
        return CategorySerializer(category).data

    def _update_category(self, category: Category, data: Dict) -> Optional[Dict]:
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return None
