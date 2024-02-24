from django.shortcuts import render, redirect, reverse
from webapp.forms import TaskForm
from webapp.models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def index_view(request):
    return render(request, 'index.html')


class TaskListView(ListView):
    model = Task
    template_name = 'partial/task_list.html'
    context_object_name = 'tasks'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect('webapp:index')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_edit.html'

    def get_success_url(self):
        return reverse('webapp:index')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_proposal_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')