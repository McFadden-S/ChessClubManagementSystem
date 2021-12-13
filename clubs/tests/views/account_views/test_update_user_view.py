"""Unit tests for the user update view."""
from django.test import TestCase
from clubs.models import User
from clubs.forms import UpdateUserForm
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next,LogInTester, NavbarTesterMixin
from django.contrib.auth.hashers import check_password
from django.contrib import messages

class UserUpdateViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for the user update view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.user2 = User.objects.get(email='bethsmith@example.org')
        self.url = reverse('update_user')
        self.form_input = {
            "first_name": "Boby",
            "last_name": "Smithy",
            "email": "bobysmithy@example.org",
            "bio": "Hiya",
            "chess_experience": "AV",
            "personal_statement": "I am Not Orangutan",
        }

    def test_user_update_url(self):
        """Test for the user update url."""

        self.assertEqual(self.url, '/update_user/')

    def test_get_user_update(self):
        """Test for getting the user update form"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateUserForm))
        self.assert_main_navbar(response)

    """Unit tests for redirecting user when not logged in"""

    def test_get_user_update_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_user_update_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_user_update(self):
        """Test to check successful user update"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        redirect_url = reverse('dashboard')
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.first_name, self.form_input['first_name'])
        self.assertTrue(self.user.last_name, self.form_input['last_name'])
        self.assertTrue(self.user.email, self.form_input['email'])
        self.assertTrue(self.user.bio, self.form_input['bio'])
        self.assertTrue(self.user.chess_experience, self.form_input['chess_experience'])
        self.assertTrue(self.user.personal_statement, self.form_input['personal_statement'])

    """Unit tests for unsuccessful user updates via name"""

    def test_unsuccessful_user_update_with_blank_first_name(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['first_name'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateUserForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.first_name == '')

    def test_unsuccessful_user_update_with_blank_last_name(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['last_name'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateUserForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.last_name == '')

    """Unit tests for unsuccessful user updates via email"""

    def test_unsuccessful_user_update_with_incorrect_email_format(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['email'] = 'notemail'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateUserForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.email == 'notemail')

    def test_unsuccessful_user_update_with_another_users_email(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['email'] = self.user2.email
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateUserForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.email == self.user2.email)
