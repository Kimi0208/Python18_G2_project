from webapp.models import Task, Proposal
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'start_date', 'updated_at', 'done_at', 'deadline',
                  'status', 'priority', 'author', 'parent_task', 'destination_to_department', 'destination_to_user',
                  'files']
        read_only_fields = ['created_at', 'updated_at', 'author']