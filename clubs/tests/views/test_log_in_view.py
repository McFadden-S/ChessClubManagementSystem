"""Unit tests of the log in view"""
from django.contrib import messages
from django.urls import reverse
from django.test import TestCase
from clubs.forms import LogInForm
from clubs.models import Club_Member, User, Club
from clubs.tests.helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    """Unit tests of the log in view"""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(
            user=self.user,
            authorization='ME',
            club=self.club
        )
        self.applicant = User.objects.get(email='bethsmith@example.org')
        Club_Member.objects.create(
            user=self.applicant,
            authorization='AP',
            club=self.club
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
        self.assertFalse(self._is_logged_in())


    def test_unsuccessful_log_in(self):
        form_input = {'email': 'bobsmith@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_successful_applicant_log_in(self):
        form_input = {'email': 'bethsmith@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_non_applicant_log_in(self):
        form_input = {'email': 'bobsmith@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)


    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        form_input = {'email': 'incorrectUser@example.org', 'password': 'inCorrectPassword123'}
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
