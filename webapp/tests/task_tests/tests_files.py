from http import HTTPStatus
from django.test import TestCase
import unittest
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from accounts.models import DefUser
from webapp.models import Task, File
from webapp.tests.factories.task import TaskFactory, StatusFactory
from webapp.forms import FileForm
from webapp.views.task_views import get_files_history


class DeleteFileViewTest(TestCase):
    def setUp(self):
        task_status = StatusFactory()
        self.user = DefUser.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(title='Test Task', status=task_status)
        self.file = File.objects.create(task=self.task, file='test.txt')

    def test_delete_file(self):
        self.client.login(username='testuser', password='12345')
        delete_url = reverse('webapp:delete_file', kwargs={'task_pk': self.task.pk, 'file_pk': self.file.pk})
        response = self.client.delete(delete_url)
        self.assertFalse(File.objects.filter(pk=self.file.pk).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_file_unauthenticated(self):
        delete_url = reverse('webapp:delete_file', kwargs={'task_pk': self.task.pk, 'file_pk': self.file.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(File.objects.filter(pk=self.file.pk).exists())


class FileAddViewTest(TestCase):
    def setUp(self):
        self.user = DefUser.objects.create_user(username='testuser', password='12345')
        self.task = TaskFactory()

    def test_file_add_view(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'name': 'test_file.txt',
        }
        response = self.client.post(reverse('webapp:add_file', kwargs={'task_pk': self.task.pk}), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(File.objects.filter(task=self.task).exists())

    # def test_file_add_view_unauthenticated(self):
    #     response = self.client.post(reverse('webapp:add_file', kwargs={'task_pk': self.task.pk}))
    #     self.assertEqual(response.status_code, 302)


#Просто проверяет работает ли функция
class GetFilesHistoryTest(unittest.TestCase):
    def test_get_files_history(self):
        files_history_list = get_files_history(task_pk=1)
        self.assertEqual(files_history_list, [])
