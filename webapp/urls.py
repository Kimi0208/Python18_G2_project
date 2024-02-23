from django.urls import path
from django.views.generic import RedirectView
from webapp.views.task_views import (
    TaskCreateView,
    TaskView,
    TaskUpdateView,
    TaskDeleteView,
    IndexView
)

app_name = "webapp"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # path("tasks/", RedirectView.as_view(pattern_name="tasks_list")),
    path("tasks/add/", TaskCreateView.as_view(), name="task_add"),
    path("task/<int:pk>", TaskView.as_view(), name="task_view"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update_view"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete_view"),
]
