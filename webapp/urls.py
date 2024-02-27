from django.urls import path

from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView, add_subtasks)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='detail_task'),
    path('task/<int:task_pk>/<int:group_pk>', add_subtasks, name='add_subtasks')
]