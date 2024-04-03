from django.urls import path
from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskView, add_subtasks,
                          FileAddView, FileDeleteView, get_task_files, get_history_task)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('tasks/<int:user_pk>/', TaskListView.as_view(), name='user_tasks'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/', TaskView.as_view(), name="task_proposal_view"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('task/<int:task_pk>/<int:checklist_pk>', add_subtasks, name='add_subtasks'),
    path('task/<int:task_pk>/file/add/', FileAddView.as_view(), name='add_file'),
    path('task/<int:task_pk>/file/<int:pk>/delete/', FileDeleteView.as_view(), name='delete_file'),
    path('task/<int:task_pk>/files/', get_task_files, name='task_file_list'),
    path('task/<int:task_pk>/create_subtask/', TaskCreateView.as_view(), name='create_subtask'),
    path('task/<int:task_pk>/history/', get_history_task, name='get_history_task')
]