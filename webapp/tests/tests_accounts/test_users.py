from django.contrib.auth import authenticate
from django.test import TestCase
from accounts.models import DefUser
from django.shortcuts import render, redirect, reverse, get_object_or_404
from webapp.tests.factories.user import DefUserFactory, DepartmentFactory, PositionFactory
from http import HTTPStatus


class TestUserDetailView(TestCase):

    def setUp(self) -> None:
        user, created = DefUser.objects.get_or_create(username='user')
        user.is_superuser = True
        user.set_password('user')
        user.save()
        self.user = user

    def test_get_detail(self):
        self.client.login(username='user', password='user')
        user = DefUserFactory()
        url = reverse("accounts:user_detail", kwargs={'pk': user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_change_user(self):
    #     self.client.login(username='user', password='user')
    #     updated_data = {
    #         'first_name': 'Test Name',
    #         'last_name': 'Test Last Name',
    #         'email': 'admin@admin.com',
    #         'email_password': '123123',
    #         'phone_number': '123123345'
    #     }
    #     user = DefUserFactory(first_name='123')
    #
    #     update_url = reverse("accounts:user_change", kwargs={'pk': user.pk})
    #     response = self.client.post(update_url, data=updated_data, follow=True)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     # updated_user = DefUser.objects.get(pk=user.pk)
    #     user.refresh_from_db()
    #
    #     self.assertEqual(user.first_name, updated_data['first_name'])
    #     # self.assertEqual(user.last_name, updated_data['last_name'])


class TestUserCreateView(TestCase):
    def test_user_create_view(self):
        user_data = {
            'username': 'User1',
            'first_name': 'Test Name',
            'last_name': 'Test Last Name',
            'email': 'admin@admin.com',
            'password': 'qweqwe'
        }
        department = DepartmentFactory()
        user_position = PositionFactory(department_id=department.id)
        new_user = DefUserFactory(username=user_data['username'], first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'], password=user_data['password'], position=user_position)
        initial_user_count = DefUser.objects.count()
        response = self.client.post(reverse('accounts:add_user'), data=user_data)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(DefUser.objects.count(), initial_user_count + 1)
        new_user = DefUser.objects.get(username='User1')
        self.assertEqual(new_user.username, user_data['username'])
        self.assertEqual(new_user.first_name, user_data['first_name'])
        self.assertEqual(new_user.last_name, user_data['last_name'])
        self.assertEqual(new_user.email, user_data['email'])
        # self.assertTrue(new_user.check_password(user_data['password']))
        # self.assertRedirects(response, reverse('accounts:user_list'))


# class TestUserUpdateView(TestCase):
#     def test_user_update_view(self):
#         existing_user = DefUserFactory()
#         updated_data = {
#             'username': 'UpdatedUser',
#             'first_name': 'Updated First Name',
#             'last_name': 'Updated Last Name',
#             'email': 'updated@admin.com',
#             'password': 'newpassword'
#         }
#         response = self.client.post(reverse('accounts:user_update', kwargs={'pk': existing_user.pk}), data=updated_data)
#         self.assertEqual(response.status_code, 200)
#         updated_user = DefUser.objects.get(pk=existing_user.pk)
#         self.assertEqual(updated_user.username, updated_data['username'])
#         self.assertEqual(updated_user.first_name, updated_data['first_name'])
#         self.assertEqual(updated_user.last_name, updated_data['last_name'])
#         self.assertEqual(updated_user.email, updated_data['email'])
#         # self.assertTrue(updated_user.check_password(updated_data['password']))


class UserDeleteViewTest(TestCase):
    def test_user_deletion(self):
        existing_user = DefUserFactory()
        initial_user_count = DefUser.objects.count()
        response = self.client.post(reverse('accounts:user_delete', kwargs={'pk': existing_user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DefUser.objects.count(), initial_user_count - 1)


# class UserPasswordChangeViewTest(TestCase):
#     def setUp(self):
#         self.user = DefUserFactory()
#         self.client.force_login(self.user)
#
#     def test_password_change(self):
#         new_password = 'newpassword'
#         response = self.client.post(reverse('accounts:password_change', kwargs={'pk': self.user.pk}), {
#             'old_password': self.user.password,
#             'new_password1': new_password,
#             'new_password2': new_password
#         })
#         self.assertEqual(response.status_code, 200)
#         user = authenticate(username=self.user.username, password=new_password)
#         self.assertIsNotNone(user)