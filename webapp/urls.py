from django.urls import path
from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskView, add_subtasks,
                          FileAddView, FileDeleteView, get_task_files, get_history_task, CommentCreateView,
                          CommentUpdateView, CommentDeleteView, get_tasks_from_id)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('tasks/user/<int:pk>/', get_tasks_from_id, name='user_tasks'),
    path('tasks/department/<int:pk>/', get_tasks_from_id, name='department_tasks'),
    path('task/create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/', TaskView.as_view(), name="task_proposal_view"),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('task/<int:task_pk>/<int:checklist_pk>/', add_subtasks, name='add_subtasks'),
    path('task/<int:task_pk>/file/add/', FileAddView.as_view(), name='add_file'),
    path('task/<int:task_pk>/file/<int:pk>/delete/', FileDeleteView.as_view(), name='delete_file'),
    path('task/<int:task_pk>/files/', get_task_files, name='task_file_list'),
    path('task/<int:task_pk>/create_subtask/', TaskCreateView.as_view(), name='create_subtask'),
    path('task/<int:task_pk>/history/', get_history_task, name='get_history_task'),
    path('task/<int:task_pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete')
]