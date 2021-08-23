from django.contrib.auth.models import User
from django.test import TestCase

from yumminess.models import Employee


class LogTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'tester',
            'password': 'secret'
        }
        self.user_test = User.objects.create_user(**self.credentials)
        Employee.objects.create(
            user=self.user_test,
            password=self.credentials['password']
        )

    def test_user(self):
        self.assertEqual(self.user_test.username, 'tester')

    def test_login(self):
        response = self.client.post('/yumminess/login', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_login_no_user(self):
        response = self.client.post('/yumminess/login', None, follow=True)

        self.assertFalse(response.context['user'].is_active)

    def test_logout(self):
        flag = False
        response_login = self.client.post('/yumminess/login', self.credentials, follow=True)
        status_login = response_login.context['user'].is_active
        response_logout = self.client.get('/yumminess/logout')
        if response_logout.context is None and status_login:
            flag = True

        self.assertTrue(flag)

    def test_logout_without_user(self):
        flag = False
        response_login = self.client.post('/yumminess/login', None, follow=True)
        status_login = response_login.context['user'].is_active
        response_logout = self.client.get('/yumminess/logout')

        if response_logout.context is None and not status_login:
            flag = True

        self.assertTrue(flag)
