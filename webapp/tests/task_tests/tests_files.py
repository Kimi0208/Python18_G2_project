from http import HTTPStatus
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
import unittest
from django.urls import reverse
from accounts.models import DefUser
from webapp.models import Task, File
from webapp.tests.factories.task import TaskFactory, StatusFactory
from webapp.views.task_views import get_files_history
from django.core.files.uploadedfile import SimpleUploadedFile


class DeleteFileViewTest(TestCase):
    def setUp(self):
        content_type = ContentType.objects.get(model="file")
        permission, created = Permission.objects.get_or_create(codename='delete_file', content_type=content_type)
        task_status = StatusFactory()
        self.user = DefUser.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(permission)
        self.task = TaskFactory(title='Test Task', status=task_status)
        self.file = File.objects.create(task=self.task, file='test.txt')

    def test_delete_file(self):
        self.client.login(username='testuser', password='12345')
        delete_url = reverse('webapp:delete_file', kwargs={'task_pk': self.task.pk, 'pk': self.file.pk})
        response = self.client.delete(delete_url)
        self.assertFalse(File.objects.filter(pk=self.file.pk).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_file_unauthenticated(self):
        new_file = File.objects.create(task=self.task, file='test.txt')
        delete_url = reverse('webapp:delete_file', kwargs={'task_pk': self.task.pk, 'pk': new_file.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(File.objects.filter(pk=new_file.pk).exists())


class FileAddViewTest(TestCase):
    def setUp(self):
        # import pdb; pdb.set_trace()
        content_type = ContentType.objects.get(model="file")
        permission, created = Permission.objects.get_or_create(codename='add_file', content_type=content_type)
        self.user = DefUser.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(permission)
        self.task = TaskFactory()

    def test_file_add_view(self):
        self.client.login(username='testuser', password='12345')
        file_content = b'Test file content'
        file = SimpleUploadedFile('test_file.txt', file_content, content_type='text/plain')
        data = {
            'file': file,
        }
        self.assertTrue(self.user.has_perm('webapp.add_file'))
        response = self.client.post(reverse('webapp:add_file', kwargs={'task_pk': self.task.pk}), data=data)
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(File.objects.filter(task=self.task).exists())

    # def test_file_add_view_unauthenticated(self):
    #     response = self.client.post(reverse('webapp:add_file', kwargs={'task_pk': self.task.pk}))
    #     self.assertEqual(response.status_code, 302)


#Просто проверяет работает ли функция
class GetFilesHistoryTest(unittest.TestCase):
    def test_get_files_history(self):
        files_history_list = get_files_history(task_pk=1)
        self.assertEqual(files_history_list, [])
