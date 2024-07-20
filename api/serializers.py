from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'date_completed', 'important', 'user']
        read_only_fields = ['created', 'date_completed']

    user = serializers.PrimaryKeyRelatedField(read_only=True)
