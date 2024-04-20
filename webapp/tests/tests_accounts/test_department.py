from django.test import TestCase
from accounts.models import DefUser, Department
from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.tests.factories.user import DefUserFactory, DepartmentFactory, PositionFactory
from http import HTTPStatus


class TestDepartmentListView(TestCase):
    def test_department_list_view(self):
        department1 = DepartmentFactory()
        department2 = DepartmentFactory()
        position1 = PositionFactory(department=department1)
        position2 = PositionFactory(department=department2)
        DefUserFactory(position=position1)
        DefUserFactory(position=position2)
        response = self.client.get(reverse('accounts:department_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('departments', response.context)
        departments = response.context['departments']
        self.assertTrue(departments)
        self.assertEqual(len(departments), Department.objects.count())
        for department in departments:
            self.assertEqual(department.num_users, department.position_set.first().defuser_set.count())


class TestDepartmentCreateView(TestCase):
    def test_department_create_view(self):
        new_department_data = {
            'name': 'Test Department',
        }
        initial_department_count = Department.objects.count()
        response = self.client.post(reverse('accounts:create_department'), data=new_department_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Department.objects.count(), initial_department_count + 1)


class TestDepartmentUpdateView(TestCase):
    def test_department_update_view(self):
        existing_department = DepartmentFactory()
        updated_department_data = {
            'name': 'Updated Department Name',
        }
        response = self.client.post(reverse('accounts:update_department', kwargs={'pk': existing_department.pk}),
                                    data=updated_department_data)
        self.assertEqual(response.status_code, 302)
        updated_department = Department.objects.get(pk=existing_department.pk)
        self.assertEqual(updated_department.name, updated_department_data['name'])


class TestDepartmentDeleteView(TestCase):
    def test_department_delete_view(self):
        existing_department = DepartmentFactory()
        initial_department_count = Department.objects.count()
        response = self.client.post(reverse('accounts:delete_department', kwargs={'pk': existing_department.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Department.objects.count(), initial_department_count - 1)