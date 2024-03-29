from django.urls import path
from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskView, add_subtasks,
                          FileAddView, FileDeleteView, get_task_files)
from webapp.views.task_views import sign_checklist

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/', TaskView.as_view(), name="task_proposal_view"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('task/<int:task_pk>/<int:checklist_pk>', add_subtasks, name='add_subtasks'),
    path('task/<int:task_pk>/file/add/', FileAddView.as_view(), name='add_file'),
    path('task/<int:task_pk>/file/<int:pk>/delete/', FileDeleteView.as_view(), name='delete_file'),
    path('task/<int:task_pk>/files/', get_task_files, name='task_file_list'),
    path('sign_checklist/<int:file_id>/', sign_checklist, name='sign_checklist'),
]