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



class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    ordering = ['-type']

    def get_queryset(self):
        # Получаем текущего пользователя
        # Если передан id пользователя в запросе, фильтруем задачи только для этого пользователя
        user_id = self.kwargs.get('user_pk')
        if user_id:
            return Task.objects.filter(author_id=user_id)
        else:
            # Возвращаем задачи текущего пользователя
            return Task.objects.filter(destination_to_user=self.request.user.pk)


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
        history_info = [(action, file_history.history_date.strftime("%d-%m-%Y %H:%M"), file_history.history_user.username, file_history.file)]
        files_history_list.append(history_info)
    return files_history_list



def get_history_task(request, task_pk):
    history_list = []
    task = Task.objects.get(pk=task_pk)
    task_history = list(task.history.all().order_by('history_date'))
    for i in range(1, len(task_history)):
        current_record = task_history[i]
        previous_record = task_history[i - 1]
        delta = current_record.diff_against(previous_record)
        change_date = current_record.history_date.strftime("%d-%m-%Y %H:%M")
        change_user = current_record.history_user
        #Если в истории можно будет оставить название поля (как записано в бд), а не verbose_name
        # changes = [(change.field, change.old, change.new, change_date, change_user) for change in delta.changes]
        changes = []
        for change in delta.changes:
            verbose_name = current_record._meta.get_field(change.field).verbose_name
            ttt = current_record._meta.get_field(change.field)
            old, new = check_is_foreign_key(ttt, change.old, change.new)
            change_info = (verbose_name, change_date, change_user.username, old, new)
            changes.append(change_info)
        # field_verbose_name = Task._meta.get_field(changes[0][0]).verbose_name
        # field_verbose_name = current_record._meta.get_field(changes[0][0]).verbose_name
        # print(f'Изменения {changes}\n')
        history_list.append(changes)
    history_list.extend(get_files_history(task_pk))
    create_record = [('Создана задача', task.created_at.strftime("%d-%m-%Y %H:%M"), task.author.username, task.title)]
    history_list.extend([(create_record)])
    if history_list:
        sorted_history = sorted(history_list, key=lambda x: x[0][1], reverse=True)
        return JsonResponse({'history': sorted_history})
    else:
        return JsonResponse({'history': history_list})

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

def get_subtasks(object):
    subtasks = Task.objects.filter(parent_task=object)
    subtasks_list = []
    destination_to = ''
    for subtask in subtasks:
        if subtask.destination_to_department:
            destination_to = subtask.destination_to_department.name
        elif subtask.destination_to_user:
            destination_to = subtask.destination_to_user.username
        subtask_data = {
            'id': subtask.id,
            'title': subtask.title,
            'destination_to': destination_to,
            'author': subtask.author.username,
            'created_at': subtask.created_at,
            'type': subtask.type.name,
            'updated_at': subtask.updated_at
        }
        subtasks_list.append(subtask_data)
    return subtasks_list


class FileDeleteView(DeleteView):
    model = File
    template_name = 'partial/file_delete.html'

    def form_valid(self, form):
        file_id = self.object.id
        self.object.delete()
        return JsonResponse({'file_id': file_id})


smtp_server = "mail.elcat.kg"
smtp_port = 465


class TaskView(DetailView):
    model = Task
    permission_required = 'webapp.view_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Checklist.objects.all()
        context['checklists'] = checklists

        # history_list = record_history(self.object.pk)
        # context['history'] = history_list
        return context

    def render_to_response(self, context, **response_kwargs):
        subtasks_list = get_subtasks(self.object)
        destination_to = ''
        if self.object.parent_task:
            if self.object.parent_task.destination_to_department:
                destination_to = self.object.parent_task.destination_to_department.name
            elif self.object.parent_task.destination_to_user:
                destination_to = self.object.parent_task.destination_to_user.username
            parent_task = {'id': self.object.parent_task.id, 'title': self.object.parent_task.title,
                           'author': self.object.parent_task.author.username,
                           'created_at': self.object.parent_task.created_at, 'destination_to': destination_to,
                           'type': self.object.parent_task.type.name, 'updated_at': self.object.parent_task.updated_at}
        else:
            parent_task = None
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
            'type': self.object.type.name,
            'parent_task': parent_task,
            'subtasks': subtasks_list,
        }
        return JsonResponse({'task':task_data})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'
    permission_required = 'webapp.add_task'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if 'task_pk' in self.kwargs:
            self.object.parent_task = Task.objects.get(pk=self.kwargs['task_pk'])
        self.object.save()
        # if self.object.destination_to_user:
        #     subject = f'CRM: Новая задача #{self.object.pk}  {self.object.title}'
        #     message = self.object.description
        #     send_email_notification(subject, message, self.object.author.email, self.object.destination_to_user.email,
        #                             smtp_server, smtp_port, self.object.author.email, self.object.author.email_password)

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
            'type': self.object.type.name,
            'destination_to_user': self.object.destination_to_user.username,
            'subtasks': get_subtasks(self.object.parent_task)
        }
        return JsonResponse(task_data)


class TaskUpdateView(UpdateView):
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
            'type': self.object.type.name,
            'subtasks': get_subtasks(self.object)
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
        file = {
            'file': self.object.file.name,
        }
        return JsonResponse({'file' : file})

