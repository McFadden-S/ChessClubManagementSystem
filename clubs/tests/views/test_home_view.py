"""Tests of the home view."""
from django.test import TestCase
from clubs.models import User,Club_Member, Club
from clubs.tests.helpers import LogInTester
from django.urls import reverse

class HomeViewTestCase(TestCase, LogInTester):
    """Tests of the home view."""
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
        self.assertEqual(self.url,'/')

    def test_get_home_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
