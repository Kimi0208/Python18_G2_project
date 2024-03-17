from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.forms import TaskForm, FileForm, CommentForm
from webapp.models import Task, Status, Priority, Type, File, Checklist, Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from docxtpl import DocxTemplate
from shutil import copyfile
from webapp.views.mail_send import send_email_notification


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    ordering = ['-type']


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_proposal_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Checklist.objects.all()
        context['checklists'] = checklists
        subtasks = Task.objects.filter(parent_task=self.object)
        context['subtasks'] = subtasks
        files = File.objects.filter(task=self.object)
        context['files'] = files
        comments = Comment.objects.filter(task=self.object)
        context['comments'] = comments
        return context


smtp_server = "mail.elcat.kg"
smtp_port = 465


# class TaskView(DetailView):
#     model = Task
#     template_name = "task_proposal_view.html"
#
#     def task_view(request, *args, pk, **kwargs):
#         task = get_object_or_404(Task, pk=pk)
#         return render(request, "task_view.html", {"task": task})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if self.object.destination_to_user:
            subject = f'CRM: Новая задача #{self.object.id}  {self.object.title}'
            message = self.object.description
            send_email_notification(subject, message, self.object.author.email, self.object.destination_to_user.email,
                                    smtp_server, smtp_port, self.object.author.email, self.object.author.email_password)
        return redirect('webapp:task_proposal_view', kwargs={'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_edit.html'

    def get_success_url(self):
        if self.object.status.name == 'Выполнена':
            if self.object.destination_to_user:
                subject = f'CRM: Задача #{self.object.id} выполнена {self.object.title}'
                message = self.object.description
                send_email_notification(subject, message, self.request.user.email, self.object.author.email,
                                        smtp_server, smtp_port, self.request.user.email,
                                        self.request.user.email_password)
        return reverse('webapp:task_proposal_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_proposal_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')


def add_subtasks(request, checklist_pk, task_pk):
    main_task = Task.objects.get(pk=task_pk)
    checklist = Checklist.objects.get(pk=checklist_pk)
    users = checklist.users.all()
    title = 'Подпись'
    description = f'Необходима подпись документа в задаче #{task_pk}'
    status = Status.objects.get(pk=1)
    priority = Priority.objects.get(pk=1)
    type = Type.objects.get(pk=1)
    for user in users:
        task = Task.objects.create(author=main_task.author, title=title, description=description, status=status,
                                   priority=priority,
                                   type=type, destination_to_user=user)
        task.parent_task = main_task
        task.save()
        subject = f'CRM: Новая подзадача #{task.id}  {task.title}'
        message = task.description
        send_email_notification(subject, message, task.author.email, user.email,
                                smtp_server, smtp_port, task.author.email, task.author.email_password)

    file_count = File.objects.count()
    doc_name = f'Задача{task_pk}_{file_count}'
    base_file_path = 'uploads/user_docs/Шаблон.docx'
    new_file_path = f'uploads/user_docs/{doc_name}.docx'
    copyfile(base_file_path, new_file_path)
    doc = DocxTemplate(new_file_path)
    context = {'title': task.title, 'description': task.description, 'users': users}
    doc.render(context)
    doc.save(new_file_path)
    File.objects.create(user=request.user, task=main_task, file=new_file_path)
    return redirect('webapp:detail_task', pk=task_pk)


class FileAddView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'file_add.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task_pk'])
        self.object.save()
        return redirect('webapp:detail_task', pk=self.object.task.pk)


class CommentAddView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task_pk'])
        self.object.author = self.request.user
        self.object.save()
        return redirect('webapp:task_proposal_view', pk=self.object.task.pk)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_update.html'

    def get_success_url(self):
        return reverse('webapp:task_proposal_view', kwargs={'pk': self.object.task.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        return reverse('webapp:task_proposal_view', kwargs={'pk': self.object.task.pk})