from webapp.forms import TaskForm
from webapp.models import Task
from django.views.generic import ListView, CreateView


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
