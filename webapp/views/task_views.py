from django.shortcuts import redirect, reverse
from webapp.forms import TaskForm, FileForm
from webapp.models import Task, Status, Priority, Type, File, Checklist
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from docxtpl import DocxTemplate
from shutil import copyfile
from webapp.views.mail_send import send_email_notification


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
    ordering = ['-type']


def record_history(task_pk):
    history_list = []
    task = Task.objects.get(pk=task_pk)
    task_history = list(task.history.all().order_by('history_date'))
    print(f'Все записи историй {task_history}\n')
    print(f'Длина списка {len(task_history)}\n')
    for i in range(1, len(task_history)):
        current_record = task_history[i]
        print(f'Запись последняя{current_record}\n')
        previous_record = task_history[i - 1]
        print(f'Запись предыдущая{previous_record}\n')
        delta = current_record.diff_against(previous_record)
        change_date = current_record.history_date.strftime("%Y-%m-%d %H:%M:%S")
        change_user = current_record.history_user
        print(delta.changes[0])
        #Если в истории можно будет оставить название поля (как записано в бд), а не verbose_name
        # changes = [(change.field, change.old, change.new, change_date, change_user) for change in delta.changes]

        changes = []
        for change in delta.changes:
            verbose_name = current_record._meta.get_field(change.field).verbose_name
            change_info = (verbose_name, change.old, change.new, change_date, change_user)
            changes.append(change_info)

        # field_verbose_name = Task._meta.get_field(changes[0][0]).verbose_name
        # field_verbose_name = current_record._meta.get_field(changes[0][0]).verbose_name
        print(f'Изменения {changes}\n')
        history_list.append(changes)
    sorted_history = sorted(history_list, key=lambda x: x[0][3], reverse=True)
    return sorted_history


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checklists = Checklist.objects.all()
        context['checklists'] = checklists
        subtasks = Task.objects.filter(parent_task=self.object)
        context['subtasks'] = subtasks
        files = File.objects.filter(task=self.object)
        context['files'] = files
        history_list = record_history(self.object.pk)
        context['history'] = history_list

        return context


smtp_server = "mail.elcat.kg"
smtp_port = 465


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_proposal_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if self.object.destination_to_user:
            subject = f'CRM: Новая задача #{self.object.id}  {self.object.title}'
            message = self.object.description
            send_email_notification(subject, message, self.object.author.email, self.object.destination_to_user.email,
                                    smtp_server, smtp_port, self.object.author.email, self.object.author.email_password)
        self.object.save()
        return redirect('webapp:index')


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
        return reverse('webapp:index')


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
        task = Task.objects.create(author=main_task.author, title=title, description=description, status=status, priority=priority,
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