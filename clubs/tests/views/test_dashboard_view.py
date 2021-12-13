"""Unit tests for the dashboard view."""
from clubs.helpers import get_all_clubs, get_my_clubs, get_other_clubs
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.test import TestCase
from django.urls import reverse


# Used this from Clucker project with some modifications
class DashboardViewTestCase(TestCase, LogInTester):
    """Unit tests for the dashboard view."""
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

    def create_my_clubs_ordered_list_by(self, order_by_var):
        my_clubs = get_my_clubs(self.user)
        sorted_list = Club.objects.filter(id__in=my_clubs).order_by(order_by_var)
        return sorted_list
    
    def create_other_clubs_ordered_list_by(self, order_by_var):
        other_clubs = get_other_clubs(self.user)
        sorted_list = Club.objects.filter(id__in=other_clubs).order_by(order_by_var)
        return sorted_list

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_clubs_list(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        my_clubs_count = get_my_clubs(self.user).count()
        other_clubs_count = get_other_clubs(self.user).count()
        all_clubs_count = get_all_clubs().count()
        self.assertEqual(all_clubs_count, (my_clubs_count + other_clubs_count))
        self.assertNotEqual(get_my_clubs(self.user), get_other_clubs(self.user))

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
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, 'My Clubs')
        self.assertNotContains(response, 'Members')
        self.assertNotContains(response, 'Applicants')


    # TODO Refactor tests to reflect javascript search/sort
    # def test_search_bar_to_filter_list(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'John Smith')
    #     self.assertContains(response, 'Beth Smith')
    #     search_bar = 'Beth'
    #     response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'Beth Smith')
    #     self.assertNotContains(response, 'John Smith')
    #
    # def test_empty_search_bar(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'John Smith')
    #     self.assertContains(response, 'Beth Smith')
    #     search_bar = ''
    #     response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertContains(response, 'Beth Smith')
    #     self.assertContains(response, 'John Smith')
    #
    # def test_sorted_list_club_name(self):
    #     sort_table = 'first_name'
    #     second_list = list(self.create_ordered_list_by(sort_table))
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     #response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     response = self.client.post(self.url, {'sort_table': sort_table})
    #     member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)
    #     members = list(User.objects.filter(id__in=member_list))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertListEqual(members, second_list)
    #
    # def test_sorted_list_city_name(self):
    #     sort_table = 'last_name'
    #     second_list = list(self.create_ordered_list_by(sort_table))
    #     self.client.login(email=self.user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     response = self.client.post(self.url, {'sort_table': sort_table})
    #     member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)
    #     members = list(User.objects.filter(id__in=member_list))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard.html')
    #     self.assertListEqual(members, second_list)
