"""Unit tests of the log in view."""
from clubs.forms import LogInForm
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.urls import reverse
from django.test import TestCase

class LogInViewTestCase(TestCase, LogInTester):
    """Unit tests of the log in view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(email='bobsmith@example.org')

    def test_log_in_url(self):
        """"Test for the log in url."""

        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in(self):
        """Test to get log in form."""

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
        """Test for unsuccessful log in with incorrect password."""

        form_input = {'email': 'bobsmith@example.org', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_user_log_in(self):
        """Test for successful log in with correct credentials."""

        form_input = {'email': 'bobsmith@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_get_log_in_with_redirect(self):
        """Test that the log in form is rendered when a user tries to go to a page that needs to be logged in."""

        destination_url = reverse('change_password')
        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_succesful_log_in_with_redirect(self):
        """Test that the user is redirected to the correct next page after successful log in."""

        redirect_url = reverse('change_password')
        form_input = { 'email': 'bobsmith@example.org', 'password': 'Password123', 'next': redirect_url }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'change_password.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    """ Unit tests to redirect when logged in """

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

    """ Unit tests to test for blank credentials """

    def test_log_in_with_blank_email(self):
        form_input = { 'email': '', 'password': 'Password123' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_log_in_with_blank_password(self):
        form_input = { 'email': 'bobsmith@example.org', 'password': '' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
