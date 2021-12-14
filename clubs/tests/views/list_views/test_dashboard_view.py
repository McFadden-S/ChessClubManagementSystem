"""Unit tests for dashboard view"""
from clubs.helpers import get_all_clubs, get_my_clubs, get_other_clubs
from clubs.models import User, Club, Club_Member
from clubs.tests.helpers import LogInTester, reverse_with_next, NavbarTesterMixin
from django.test import TestCase
from django.urls import reverse


# Used this from Clucker project with some modifications
class DashboardViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for dashboard view"""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.second_user = User.objects.get(email='bethsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_owner = Club_Member.objects.create(
            user=self.user, authorization='OW', club=self.club
        )
        self.second_club = Club.objects.get(name='Flying Orangutans 2')
        self.second_club_owner = Club_Member.objects.create(
            user=self.second_user, authorization='OW', club=self.club
        )
        self.url = reverse('dashboard')

    """Create ordered list to compare with"""

    def create_my_clubs_ordered_list_by(self, order_by_var):
        my_clubs = get_my_clubs(self.user)
        sorted_list = Club.objects.filter(id__in=my_clubs).order_by(order_by_var)
        return sorted_list

    def create_other_clubs_ordered_list_by(self, order_by_var):
        other_clubs = get_other_clubs(self.user)
        sorted_list = Club.objects.filter(id__in=other_clubs).order_by(order_by_var)
        return sorted_list

    def test_dashboard_url(self):
        """Test for the show applicant url"""

        self.assertEqual(self.url, '/dashboard/')

    def test_get_clubs_list(self):
        """Test get list of clubs"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        my_clubs_count = get_my_clubs(self.user).count()
        other_clubs_count = get_other_clubs(self.user).count()
        all_clubs_count = get_all_clubs().count()
        self.assertEqual(all_clubs_count, (my_clubs_count + other_clubs_count))
        self.assertNotEqual(get_my_clubs(self.user), get_other_clubs(self.user))

    """Unit tests to redirect when not logged in"""

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_post_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_dashboard_navbar(self):
        """Test dashboard navbar contents"""

        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, 'My Clubs')
        self.assertNotContains(response, 'Members')
        self.assertNotContains(response, 'Applicants')
