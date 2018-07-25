from django.test import TestCase
from django.contrib.auth import get_user_model

class LogInTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {
            'username': 'testuser1',
            'password': 'ashwani1'
        }
        User.objects.create(**self.credentials)

    def test_login(self):
        response = self.client.post('/blog/login/', self.credentials)
        self.assertTrue(response.context['user'])

class SignupTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.details = {
            'username': 'newuser1',
            'password': 'ashwani1'
        }
        User.objects.create(**self.details)

    def test_signup(self):
        response = self.client.post('/blog/signup/editor/', self.details, follow=True)
        self.assertTrue(response.context['user'])


# class PostNewTest(TestCase):
#     def setUp(self):
