"""Tests of the log out view."""

from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import LogInTester, reverse_with_next

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(email='bobsmith@example.org')

    def test_log_out_url(self):
        """Test for the log out url."""

        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        """Test for the user successfully logging out."""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())

    def test_get_log_out_redirects_when_not_logged_in(self):
        """Test for the user not being able to log out when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
