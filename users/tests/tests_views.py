from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersLoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login(self):
        # send login data
        response = self.client.post('/users/login/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_correct_redirect(self):
        response = self.client.post('/users/login/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'http://127.0.0.1:8000')


class LogoutViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        self.client.login(username='testuser', password="secret")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/logout/', follow=True)
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'), follow=True)
        assert response.status_code == 200

    def test_logout_correct_redirect(self):
        response = self.client.get('/users/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/users/login/')

    def test_logout(self):
        # send login data
        response = self.client.post('/users/logout/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        # should be logged in now
        self.assertFalse(response.context['user'].is_authenticated)
