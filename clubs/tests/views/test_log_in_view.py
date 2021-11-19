"""Unit tests of the log in view"""
from django.contrib import messages
from django.urls import reverse
from django.test import TestCase
from clubs.forms import LogInForm
from clubs.models import User

class LogInViewTestCase(TestCase):
    """Unit tests of the log in view"""
    def setUp(self):
        self.url = reverse('log_in')
        User.objects.create_user(email='orangutan@example.org',
            first_name='orang',
            last_name='utan',
            bio='I am a smart orangutan',
            chess_experience='Beginner',
            personal_statement='I would love to learn how to play chess',
            password='CorrectPassword123'
        )

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_input = {'email': 'orangutan@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        form_input = {'email': 'orangutan@example.org', 'password': 'CorrectPassword123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('members_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
