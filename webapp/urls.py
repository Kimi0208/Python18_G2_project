from django.urls import path

from webapp.views.task_views import TaskListView, TaskDetailView

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view()),
    path('home/', TaskListView.as_view(), name='home'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]
