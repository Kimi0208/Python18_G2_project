from django.views.generic import ListView, DetailView, CreateView
from webapp.models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    pass
