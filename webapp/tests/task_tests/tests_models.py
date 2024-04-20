from django.test import TestCase
from http import HTTPStatus
from webapp.models import Task, Type, Status
from accounts.models import DefUser, Department
from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.tests.factories.task import TaskFactory, TypeFactory, StatusFactory, PriorityFactory
from webapp.tests.factories.user import DefUserFactory, DepartmentFactory
from webapp.views.task_views import get_object_from_model, check_is_foreign_key


class GetObjectFromModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user, created = DefUser.objects.get_or_create(username='user', is_superuser=True)
        user.set_password('user')
        user.save()
        cls.user = user

    def setUp(self):
        self.status = StatusFactory()

        self.obj1 = Task.objects.create(title='Object 1', status=self.status)
        self.obj2 = Task.objects.create(title='Object 2', status=self.status)

    def test_get_object_from_model_exists(self):
        result = get_object_from_model(Task, self.obj1.pk)
        self.assertEqual(result, self.obj1)

    def test_get_object_from_model_does_not_exist(self):
        result = get_object_from_model(Task, 1000)
        self.assertIsNone(result)


class CheckIsForeignKeyTest(TestCase):
    def setUp(self):
        self.task = TaskFactory()
        self.status = StatusFactory()

    def test_foreign_key_field(self):
        field = Task._meta.get_field('status')
        old_value = self.task.status.pk if self.task.status else None
        new_value = self.status.pk
        old_obj, new_obj = check_is_foreign_key(field, old_value, new_value)

        self.assertEqual(old_obj, self.task.status)
        self.assertEqual(new_obj, self.status)

    def test_non_foreign_key_field(self):
        field = Task._meta.get_field('title')
        old_value = 'old_value'
        new_value = 'new_value'
        old_result, new_result = check_is_foreign_key(field, old_value, new_value)
        self.assertEqual(old_result, old_value)
        self.assertEqual(new_result, new_value)
