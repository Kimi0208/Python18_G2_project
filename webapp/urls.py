from django.urls import path

from webapp.views import TaskListView, TaskCreateView

app_name = 'webapp'

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('create/', TaskCreateView.as_view(), name='create_task')
]