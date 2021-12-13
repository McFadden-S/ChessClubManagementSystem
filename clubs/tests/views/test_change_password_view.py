"""Unit tests for change_password view"""
from clubs.forms import UserChangePasswordForm
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next, NavbarTesterMixin
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse


# Used this from clucker project with some modifications
class UserChangePasswordViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for change_password view"""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(
            user=self.user,
            club=self.club
        )
        self.url = reverse('change_password')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'new_password_confirmation': 'NewPassword123',
        }

    def test_change_password_url(self):
        """Test for the change password url"""
        self.assertEqual(self.url, '/change_password/')

    def test_get_change_password(self):
        """Test get change password"""
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """Unit tests for password change redirects"""
    def test_get_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_successful_password_change(self):
        """Test for successful password change"""
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 1)

    """Unit tests for unsuccessful password change"""

    def test_password_change_unsuccessful_with_incorrect_old_password(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_password_change_unsuccessful_without_password_confirmation(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['new_password_confirmation'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_change_password_navbar(self):
        """Test for navbar content"""
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        #self.assert_no_club_navbar(response)
        # self.assertContains(response, 'My Clubs')
        # self.assertNotContains(response, 'Members')
        # self.assertNotContains(response, 'Applicants')
