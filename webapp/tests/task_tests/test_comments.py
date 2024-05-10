from http import HTTPStatus
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
import unittest
from django.urls import reverse
from accounts.models import DefUser
from webapp.models import Task, File, Comment
from webapp.tests.factories.task import TaskFactory, StatusFactory
from webapp.tests.factories.comment import CommentFactory
from webapp.views.task_views import get_files_history


class CommentViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        content_type = ContentType.objects.get(model="file")
        permission, created = Permission.objects.get_or_create(codename='add_comment', content_type=content_type)
        task_status = StatusFactory()
        cls.type = StatusFactory()
        cls.status = StatusFactory()
        user, created = DefUser.objects.get_or_create(username='user')
        user.is_superuser = True
        user.set_password('user')
        user.save()
        user.user_permissions.add(permission)
        cls.user = user

    def setUp(self):
        self.client.login(username='user', password='user')
        self.task = TaskFactory()
        self.comment = CommentFactory(task=self.task, author=self.user)

    def test_comment_create_view(self):
        data = {
            'description': 'Test Comment Description'
        }
        url = reverse('webapp:comment_create', kwargs={'task_pk': self.task.pk})
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(description='Test Comment Description').exists())
        comment = Comment.objects.get(description='Test Comment Description')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.task, self.task)

    def test_comment_update_view(self):
        updated_description = 'Updated Comment Description'
        data = {
            'description': updated_description
        }
        url = reverse('webapp:comment_update', kwargs={'pk': self.comment.pk})
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.description, updated_description)
        self.assertEqual(response.json()["comment"]["description"], updated_description)
        self.assertEqual(response.json()["comment"]["author_id"], self.user.id)
        self.assertEqual(response.json()["comment"]["task"], self.task.id)
        self.assertEqual(response.json()["comment"]["id"], self.comment.id)
        self.assertEqual(response.json()["comment"]["author_first_name"], self.user.first_name)
        self.assertEqual(response.json()["comment"]["author_last_name"], self.user.last_name)

    def test_comment_delete_view(self):
        url = reverse('webapp:comment_delete', kwargs={'pk': self.comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Comment.objects.filter(pk=self.comment.pk).exists())
