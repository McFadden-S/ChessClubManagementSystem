"""Unit tests for the applicant list view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, NavbarTesterMixin, reverse_with_next
from django.test import TestCase
from django.urls import reverse
from django.contrib import messages


# Used this from clucker project with some modifications
class ApplicantListViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for the applicant list view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='harrysmith@example.org')
        self.officer = User.objects.get(email='bobsmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        Club_Member.objects.create(
            user=self.member, authorization='ME', club=self.club
        )
        Club_Member.objects.create(
            user=self.applicant, authorization='AP', club=self.club
        )

        self.url = reverse('applicants_list', kwargs={'club_id': self.club.id})

    def test_applicants_list_url(self):
        """Test for the applicant list url."""

        self.assertEqual(self.url, f'/{self.club.id}/applicants_list/')

    def test_get_applicants_list_redirects_when_not_logged_in(self):
        """Test for redirecting when not logged in"""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    """ Unit tests for showing applicant list """

    def test_get_applicants_list_by_owner(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicants_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_main_navbar(response)
        self.assert_club_navbar(response, self.club.id)

    def test_get_applicants_list_by_officer(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicants_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_main_navbar(response)
        self.assert_club_navbar(response, self.club.id)

    def test_get_applicants_list_redirects_user_when_authorization_is_member(self):
        """Test for redirecting member to member list from applicant list"""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_applicants_list_redirects_user_when_authorization_is_applicant(self):
        """Test for redirecting applicant to waiting list from applicant list"""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
