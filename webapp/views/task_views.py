from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect, reverse, render
from webapp.forms import TaskForm, FileForm
from webapp.models import Task, Status, Priority, Type, File, Checklist
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from docxtpl import DocxTemplate
from shutil import copyfile
from webapp.views.mail_send import send_email_notification
from django.db.models import ForeignKey
import json

from docx import Document
from docx.shared import Inches


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    ordering = ['-type']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checklists'] = Checklist.objects.all()
        return context


def get_object_from_model(model, value):
    try:
        return model.objects.get(pk=value)
    except model.DoesNotExist:
        return None


def check_is_foreign_key(field, old_value, new_value):
    if isinstance(field, ForeignKey):
        # if old_value is not None:
        #     old_obj_name = field.related_model.objects.get(pk=old_value)
        # else:
        #     old_obj_name = None
        # if new_value is not None:
        #     new_obj_name = field.related_model.objects.get(pk=new_value)
        # else:
        #     new_obj_name = None
        old_obj_name = get_object_from_model(field.related_model, old_value)
        new_obj_name = get_object_from_model(field.related_model, new_value)

        return old_obj_name, new_obj_name
    else:
        return old_value, new_value


# def get_files_history(task):
#     try:
#         files_history = []
#         files = File.objects.filter(task=task)
#         print(files)
#         for file in files:
#             task_file_history = file.history.all()
#             for history in task_file_history:
#                 action = ""
#                 if history.history_type == '+':
#                     action = "Добавлен файл"
#                 elif history.history_type == '-':
#                     action = "Удален файл"
#                 history_info = (action, history.history_date.strftime("%Y-%m-%d %H:%M:%S"), history.history_user, file.file.name)
#                 files_history.append(history_info)
#         print(files_history)
#         return files_history
#     except File.DoesNotExist:
#         pass

# def get_files_history(task_pk):
#     files_history_list = []
#     files = File.objects.filter(task_id=task_pk)
#     for file in files:
#         file_history = file.history.all()
#         for history in file_history:
#             action = ""
#             if history.history_type == "+":
#                 action = "Добавлен файл"
#             elif history.history_type == "-":
#                 action = "Удален файл"
#             history_info = [(action, history.history_date.strftime("%Y-%m-%d %H:%M:%S"), history.history_user, history.file)]
#             files_history_list.append(history_info)
#     return files_history_list

def get_files_history(task_pk):
    files_history_list = []
    files_history = File.history.filter(task_id=task_pk)
    for file_history in files_history:
        action = ""
        if file_history.history_type == "+":
            action = "Добавлен файл"
        elif file_history.history_type == "-":
            action = "Удален файл"
        history_info = [(action, file_history.history_date.strftime("%Y-%m-%d %H:%M:%S"), file_history.history_user,
                         file_history.file)]
        files_history_list.append(history_info)
    return files_history_list


def record_history(task_pk):
    history_list = []
    task = Task.objects.get(pk=task_pk)
    task_history = list(task.history.all().order_by('history_date'))
    for i in range(1, len(task_history)):
        current_record = task_history[i]
        previous_record = task_history[i - 1]
        delta = current_record.diff_against(previous_record)
        change_date = current_record.history_date.strftime("%Y-%m-%d %H:%M:%S")
        change_user = current_record.history_user
        # Если в истории можно будет оставить название поля (как записано в бд), а не verbose_name
        # changes = [(change.field, change.old, change.new, change_date, change_user) for change in delta.changes]
        changes = []
        for change in delta.changes:
            verbose_name = current_record._meta.get_field(change.field).verbose_name
            ttt = current_record._meta.get_field(change.field)
            old, new = check_is_foreign_key(ttt, change.old, change.new)
            change_info = (verbose_name, change_date, change_user, old, new)
            changes.append(change_info)
        # field_verbose_name = Task._meta.get_field(changes[0][0]).verbose_name
        # field_verbose_name = current_record._meta.get_field(changes[0][0]).verbose_name
        # print(f'Изменения {changes}\n')
        history_list.append(changes)
    history_list.extend(get_files_history(task_pk))
    if history_list:
        sorted_history = sorted(history_list, key=lambda x: x[0][1], reverse=True)
        return sorted_history
    else:
        return history_list


def get_task_files(request, task_pk):
    files = File.objects.filter(task=task_pk)
    file_list = []
    for file in files:
        file_data = {
            'id': file.id,
            'name': file.file.name,
            'task_id': file.task.id,
            'url': file.file.url
        }
        file_list.append(file_data)
    print(file_list)
    return JsonResponse({'files': file_list})


class FileDeleteView(DeleteView):
    model = File
    template_name = 'partial/file_delete.html'

    def form_valid(self, form):
        doc_name = self.object.file.path.split('/')[-1].split('.')[0]
        Task.objects.filter(description__icontains=doc_name).delete()

        file_id = self.object.id
        self.object.delete()
        return JsonResponse({'file_id': file_id})


smtp_server = "mail.elcat.kg"
smtp_port = 465


class TaskView(PermissionRequiredMixin, DetailView):
    model = Task
    permission_required = 'webapp.view_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Checklist.objects.all()
        context['checklists'] = checklists
        subtasks = Task.objects.filter(parent_task=self.object)
        context['subtasks'] = subtasks
        files = File.objects.filter(task=self.object)
        context['files'] = files
        # history_list = record_history(self.object.pk)
        # context['history'] = history_list

        # Получаем список пользователей, включенных в чеклист текущей задачи
        checklist_users = []
        for checklist in checklists:
            checklist_users.extend(checklist.users.all())
        context['checklist_users'] = checklist_users

        return context

    def render_to_response(self, context, **response_kwargs):
        task_data = {
            'id': self.object.pk,
            'title': self.object.title,
            'description': self.object.description,
            'created_at': self.object.created_at,
            'start_date': self.object.start_date,
            'updated_at': self.object.updated_at,
            'done_at': self.object.done_at,
            'deadline': self.object.deadline,
            'status': self.object.status.name,
            'priority': self.object.priority.name,
            'author': self.object.author.username,
            'type': self.object.type.name
        }
        if len(self.object.files.all()):
            task_data['files'] = True
            for i in self.object.files.all():
                task_data['signing_user'] = True if self.request.user in i.checklist.users.all() else False
        return JsonResponse({'task': task_data})


class TaskCreateView(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'
    permission_required = 'webapp.add_task'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if self.object.destination_to_user:
            subject = f'CRM: Новая задача #{self.object.pk}  {self.object.title}'
            message = self.object.description
            send_email_notification(subject, message, self.object.author.email, self.object.destination_to_user.email,
                                    smtp_server, smtp_port, self.object.author.email, self.object.author.email_password)

        task_data = {
            'id': self.object.pk,
            'title': self.object.title,
            'description': self.object.description,
            'created_at': self.object.created_at,
            'start_date': self.object.start_date,
            'updated_at': self.object.updated_at,
            'done_at': self.object.done_at,
            'deadline': self.object.deadline,
            'status': self.object.status.name,
            'priority': self.object.priority.name,
            'author': self.object.author.username,
            'type': self.object.type.name
        }
        return JsonResponse(task_data)


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_edit.html'
    permission_required = 'webapp.change_task'

    def form_valid(self, form):
        self.object = form.save()
        if self.object.status.name == 'Выполнена':
            if self.object.destination_to_user:
                subject = f'CRM: Задача #{self.object.id} выполнена {self.object.title}'
                message = self.object.description
                send_email_notification(subject, message, self.request.user.email, self.object.author.email,
                                        smtp_server, smtp_port, self.request.user.email,
                                        self.request.user.email_password)
        task_data = {
            'id': self.object.pk,
            'title': self.object.title,
            'description': self.object.description,
            'start_date': self.object.start_date,
            'updated_at': self.object.updated_at,
            'done_at': self.object.done_at,
            'deadline': self.object.deadline,
            'status': self.object.status.name,
            'priority': self.object.priority.name,
            'type': self.object.type.name
        }
        return JsonResponse(task_data)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_proposal_delete.html'

    def get_success_url(self):
        return reverse('webapp:index')


def add_subtasks(request, checklist_pk, task_pk):
    main_task = Task.objects.get(pk=task_pk)
    checklist = Checklist.objects.get(pk=checklist_pk)
    users = checklist.users.all()

    file_count = File.objects.count()
    doc_name = f'Задача{task_pk}_{file_count + 1}'
    base_file_path = 'uploads/user_docs/Шаблон.docx'
    new_file_path = f'uploads/user_docs/{doc_name}.docx'

    title = 'Подпись'
    description = f'Необходима подпись документа {doc_name} в задаче #{task_pk}'
    status = Status.objects.get(pk=1)
    priority = Priority.objects.get(pk=1)
    type = Type.objects.get(pk=1)
    for user in users:
        task = Task.objects.create(author=main_task.author, title=title, description=description, status=status,
                                   priority=priority,
                                   type=type, destination_to_user=user)
        task.parent_task = main_task
        task.save()
        # subject = f'CRM: Новая подзадача #{task.id}  {task.title}'
        # message = task.description
        # send_email_notification(subject, message, task.author.email, user.email,
        #                         smtp_server, smtp_port, task.author.email, task.author.email_password)


    copyfile(base_file_path, new_file_path)
    doc = DocxTemplate(new_file_path)
    context = {'title': task.title, 'description': task.description, 'users': users}
    doc.render(context)
    doc.save(new_file_path)
    File.objects.create(user=request.user, task=main_task, file=new_file_path, checklist=checklist_pk)
    return HttpResponse(status=200)


class FileAddView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'file_add.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.task = Task.objects.get(pk=self.kwargs['task_pk'])
        self.object.save()
        file = {
            'file': self.object.file.name,
        }
        return JsonResponse({'file': file})



def sign_checklist(request, file_id):
    checklist_file = get_object_or_404(File, pk=file_id)

    signature_path = 'uploads/signature/test.png'

    doc = Document(checklist_file.file)

    current_user = request.user
    current_user_id = str(current_user.id)

    if current_user.signature:
        signature_path = current_user.signature.path

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if current_user_id in cell.text:
                    paragraph = cell.paragraphs[0]
                    run = paragraph.add_run()
                    run.add_picture(signature_path, width=Inches(2))

    doc.save(checklist_file.file.path)

    task_id = checklist_file.task_id

    return HttpResponseRedirect(reverse('webapp:detail_task', kwargs={'pk': task_id}))
