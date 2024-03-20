from django.urls import path

from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, add_subtasks,
                          FileAddView, CommentAddView, TaskDetailView, CommentUpdateView, CommentDeleteView,
                          FileDeleteView)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>', TaskDetailView.as_view(), name="task_proposal_view"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='detail_task'),
    path('task/<int:task_pk>/<int:checklist_pk>', add_subtasks, name='add_subtasks'),
    path('task/<int:task_pk>/file/add', FileAddView.as_view(), name='add_file'),
    path('task/<int:task_pk>/comments/add', CommentAddView.as_view(), name='add_comment'),
    path('comments/<int:pk>/update', CommentUpdateView.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete', CommentDeleteView.as_view(), name='delete_comment'),
    path('file/<int:pk>/delete', FileDeleteView.as_view(), name='file_delete')
]
