from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.forms import TaskForm
from webapp.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'


class TaskView(DetailView):
    model = Task
    template_name = "task_proposal_view.html"

    def task_view(request, *args, pk, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        return render(request, "task_proposal_view.html", {"task": task})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:task_proposal_view', kwargs={'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_edit.html'

    def get_success_url(self):
        return reverse('webapp:task_proposal_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_proposal_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')


