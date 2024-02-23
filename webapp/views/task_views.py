from django.shortcuts import render, reverse, redirect, get_object_or_404
from webapp.models import Task
from webapp.forms import TaskForm
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView


class IndexView(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskView(DetailView):
    model = Task
    template_name = "tasks/task_view.html"


def task_view(request, *args, pk, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_view.html", {"task": task})


class TaskCreateView(CreateView):
    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        # form.save_m2m()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    template_name = "tasks/task_update.html"
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"

    def get_success_url(self):
        return reverse('webapp:index')