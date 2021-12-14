"""Unit tests for members list"""
from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from clubs.tests.helpers import LogInTester, NavbarTesterMixin
from django.contrib import messages


# Used this from clucker project with some modifications
class MembersListViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for members list"""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='harrysmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        Club_Member.objects.create(
            user=self.member, authorization='ME', club=self.club
        )
        Club_Member.objects.create(
            user=self.applicant, authorization='AP', club=self.club
        )

        self.url = reverse('members_list', kwargs={'club_id': self.club.id})

    def test_members_list_url(self):
        """Test for the members list url"""

        self.assertEqual(self.url, f'/{self.club.id}/members_list/')

    def test_get_members_list_redirects_when_not_logged_in(self):
        """Test get redirect when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_members_list_redirects_when_not_logged_in(self):
        """Test post redirect when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    """ Unit tests for showing members list """

    def test_get_members_list_by_owner(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_main_navbar(response)
        self.assert_club_navbar(response, self.club.id)

    def test_get_members_list_by_officer(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_main_navbar(response)
        self.assert_club_navbar(response, self.club.id)

    def test_get_members_list_by_member(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_main_navbar(response)
        self.assert_club_navbar(response, self.club.id)

    def test_get_members_list_by_applicant(self):
        """Test for redirecting applicant to waiting list from members list."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
