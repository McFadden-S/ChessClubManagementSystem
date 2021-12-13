"""Unit tests for show club view."""
from clubs.models import Club, User
from clubs.tests.helpers import LogInTester, NavbarTesterMixin, reverse_with_next
from django.test import TestCase
from django.urls import reverse

class ShowClubViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for show club view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.url = reverse('show_club', kwargs={'club_id': self.club.id})

    def test_show_club_url(self):
        """Test for the show club url."""

        self.assertEqual(self.url, f'/show_club/{self.club.id}')

    def test_get_show_club_by_any_user(self):
        """Test for getting show club page by any user"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Club Info")
        self.assertContains(response, "Flying Orangutans")


    def test_get_show_club_redirects_when_not_logged_in(self):
        """Test get show club redirects to login when not logged in"""

        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_post_show_club_redirects_when_not_logged_in(self):
        """Test post show club redirects to login when not logged in"""

        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    """Unit tests to get show applicant with valid and invalid id"""

    def test_get_show_club_with_valid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.assertContains(response, "Flying Orangutans")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        url = reverse('show_club', kwargs={'club_id': self.club.id+9999})
        response = self.client.get(url, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
