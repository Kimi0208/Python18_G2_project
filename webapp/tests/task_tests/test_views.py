from unittest import mock
from django.test import TestCase
from http import HTTPStatus
from webapp.models import Task, Type, Status, Checklist
from accounts.models import DefUser, Department
from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.tests.factories.task import TaskFactory, TypeFactory, StatusFactory, PriorityFactory
from webapp.tests.factories.user import DefUserFactory, DepartmentFactory
from webapp.views.task_views import get_files_history
from webapp.views import mail_send


class TaskViewsTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.type = StatusFactory
        cls.status = StatusFactory
        user, created = DefUser.objects.get_or_create(username='user')
        # if created:
        user.is_superuser = True
        user.set_password('user')
        user.save()
        cls.user = user



    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_task_create_view(self):
        self.client.login(username='user', password='user')
        task_type = TypeFactory()
        task_status = StatusFactory()
        task_priority = PriorityFactory()
        task_user_department = DepartmentFactory()
        task_user = DefUserFactory()
        task = TaskFactory(type=task_type, status=task_status)
        data = {
            'title': 'Task 1',
            'type': task_type.id,
            'description': 'Test description',
            'status': task_status.id,
            'start_date': '2024-04-04T19:35:02',
            'done_at': '2024-04-04 19:35:02',
            'deadline': '2024-04-04T19:43',
            'priority': task_priority.id,
            'destination_to_department': task_user_department.id,
            'destination_to_user': task_user.id
        }
        response = self.client.post('/create/', data=data)
        # print(response.content)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get(title='Task 1')
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.status.id, task_status.id)

    def test_task_update_view(self):
        self.client.login(username='user', password='user')
        task_type = TypeFactory()
        task_status = StatusFactory()
        task_priority = PriorityFactory()
        task_user_department = DepartmentFactory()
        task_user = DefUserFactory()
        task = TaskFactory(type=task_type, status=task_status)
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'type': task_type.id,
            'status': task_status.id,
            'start_date': '2024-04-04T19:35:02',
            'done_at': '2024-04-04 19:35:02',
            'deadline': '2024-04-04T19:43',
            'priority': task_priority.id,
            'destination_to_department': task_user_department.id,
            'destination_to_user': task_user.id
        }

        update_url = reverse('webapp:update_task', kwargs={'pk': task.pk})
        response = self.client.post(update_url, data=updated_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        updated_task = Task.objects.get(pk=task.pk)
        self.assertEqual(updated_task.title, updated_data['title'])
        self.assertEqual(updated_task.description, updated_data['description'])
        self.assertEqual(updated_task.type.id, task_type.id)
        self.assertEqual(updated_task.status.id, task_status.id)

    def test_task_detail_view(self):
        self.client.login(username='user', password='user')
        task_type = TypeFactory()
        task_status = StatusFactory()

        task = TaskFactory(type=task_type, status=task_status)
        detail_url = reverse('webapp:task_proposal_view', kwargs={'pk': task.pk})
        response = self.client.get(detail_url)
        # print(response.content.decode())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(task.title in response.content.decode())
        self.assertTrue(task.description in response.content.decode())
        # self.assertTrue(task_type.name in response.content.decode())
        self.assertTrue(task_status.name in response.content.decode())

    def test_task_delete_view(self):
        self.client.login(username='user', password='user')
        task_type = TypeFactory()
        task_status = StatusFactory()

        task = TaskFactory(type=task_type, status=task_status)
        delete_url = reverse('webapp:delete_task', kwargs={'pk': task.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.count(), 0)

    def test_index_view(self):
        self.client.login(username='user', password='user')

        task_type = TypeFactory()
        task_status = StatusFactory()
        TaskFactory.create_batch(5, type=task_type, status=task_status)

        index_url = reverse('webapp:index')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Task.objects.count(), 5)
        self.assertContains(response, '<tr class="task">', count=5)


class AddSubtasksTestCase(TestCase):
    def setUp(self):
        user, created = DefUser.objects.get_or_create(username='user')
        user.is_superuser = True
        user.set_password('user')
        user.save()
        self.user = user
        self.main_task = Task.objects.create(author=self.user, title='Основная задача', description='Описание основной задачи')
        self.checklist = Checklist.objects.create(name='Тестовый чеклист')
        self.checklist.users.add(self.user)

    @mock.patch("webapp.views.task_views.send_email_notification", return_value='ok')
    def test_add_subtasks(self, mock_function):
        self.client.login(username='user', password='user')
        task_status = StatusFactory()
        task_priority = PriorityFactory()
        task_type = TypeFactory()
        url = reverse('webapp:add_subtasks', kwargs={'task_pk': self.main_task.pk, 'checklist_pk': self.checklist.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        subtasks = Task.objects.filter(parent_task=self.main_task)
        self.assertEqual(subtasks.count(), self.checklist.users.count())

    def tearDown(self):
        Task.objects.all().delete()
        Checklist.objects.all().delete()
        DefUser.objects.all().delete()

