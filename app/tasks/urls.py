from django.urls import path

from .views import (
    TaskCrudAPIView,
    TaskDetailAPIView,
    CategoryCrudAPIView,
    CategoryDetailAPIView,
)


urlpatterns = [
    path("tasks/", TaskCrudAPIView.as_view(), name="task-list-create"),
    path("tasks/<str:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
    path("categories/", CategoryCrudAPIView.as_view(), name="category-list-create"),
    path("categories/<str:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
]
