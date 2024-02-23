from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from webapp.forms import TaskForm
from webapp.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template import loader


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
        self.object.save()
        return redirect('webapp:index')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_edit.html'

    def get_success_url(self):
        return reverse('webapp:index')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')