from django.urls import path

from webapp.views import (TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskView)

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>', TaskView.as_view(), name="task_proposal_view"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
]