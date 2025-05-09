from rest_framework import serializers

from .category import CategorySerializer
from tasks.models import Task, Category


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source="category"
    )

    class Meta:
        model = Task
        fields = [
            "id", "title", "due_date", "created_at",
            "updated_at", "user", "category", "category_id", "is_done"
        ]

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category = validated_data.pop("category", None)
        instance = super().update(instance, validated_data)
        if category:
            instance.category = category
        instance.save()
        return instance
