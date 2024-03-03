from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from webapp.forms import TaskForm
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
    model = Task
    form_class = TaskForm
    template_name = 'task/task_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:task_detail', kwargs={'pk': self.object.pk})