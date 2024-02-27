from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from webapp.forms import TaskForm
from webapp.models import Task, Status, Priority, Type
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.models import DefUser


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Group.objects.all()
        context['checklists'] = checklists
        subtasks = Task.objects.filter(parent_task=self.object)
        context['subtasks'] = subtasks
        return context


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


def add_subtasks(request, group_pk, task_pk):
    group1 = Group.objects.get(pk=group_pk)
    users = DefUser.objects.filter(groups=group1)
    title = 'Подпись'
    description = ''
    status = Status.objects.get(pk=1)
    priority = Priority.objects.get(pk=1)
    type = Type.objects.get(pk=1)
    for user in users:
        task = Task.objects.create(author=user, title=title, description=description, status=status, priority=priority,
                                   type=type)
        main_task = Task.objects.get(pk=task_pk)
        task.parent_task = main_task
        task.save()
    return redirect('webapp:index')
