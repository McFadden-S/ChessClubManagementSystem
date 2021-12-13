"""Unit tests for home view"""
from clubs.models import User, Club, Club_Member
from clubs.tests.helpers import LogInTester, NavbarTesterMixin
from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for home view"""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_applicant = Club_Member.objects.create(
            user=self.user, authorization='AP', club=self.club
        )

    def test_get_home_page(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self._is_logged_in())

    def test_home_url(self):
        """Test for the home url."""
        self.assertEqual(self.url, '/')

    def test_get_home_redirects_when_logged_in(self):
        """Test get redirects when not logged in"""
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        self.assert_main_navbar(response)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_home_navbar(self):
        """Test home navbar contents"""
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertNotContains(response, 'My Clubs')
        self.assertNotContains(response, 'Members')
        self.assertNotContains(response, 'Applicants')
