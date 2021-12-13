from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, NavbarTesterMixin
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password
from django.contrib import messages


# Used this from clucker project with some modifications
class ApplicantListViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    # Import default users and club.
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        # Setup
        self.owner = User.objects.get(email='harrysmith@example.org')
        self.officer = User.objects.get(email='bobsmith@example.org')
        self.applicant = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        self.club_owner = Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        self.club_member = Club_Member.objects.create(
            user=self.member, authorization='ME', club=self.club
        )
        self.club_applicant = Club_Member.objects.create(
            user=self.applicant, authorization='AP', club=self.club
        )

        self.url = reverse('waiting_list', kwargs={'club_id': self.club.id})

    def test_waiting_list_url(self):
        """"Test for the waiting list url."""

        self.assertEqual(self.url, f'/{self.club.id}/waiting_list/')

    def test_waiting_list_content_when_signed_in_as_applicant(self):
        """"Test content of waiting list for applicant"""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'waiting_list.html')
        self.assert_main_navbar(response)
        # add test for message
        # add test mixin to check logout
        self.assertEqual(response.status_code, 200)

    # Redirects

    def test_waiting_list_redirects_to_members_list_when_signed_in_as_member(self):
        """Test redirect to member list for member."""

        # shows message You are not an applicant
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        # doesnt work with assertRedirects
        # self.assert_main_navbar(response)
        # messages_list = list(response.context['messages'])
        # self.assertEqual(len(messages_list), 1)
        # self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_waiting_list_redirects_to_members_list_when_signed_in_as_officer(self):
        """Test redirect to member list for officer."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        # self.assert_main_navbar(response)
        # messages_list = list(response.context['messages'])
        # self.assertEqual(len(messages_list), 1)
        # self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_waiting_list_redirects_to_members_list_when_signed_in_as_owner(self):
        """Test redirect to member list for owner."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        # self.assert_main_navbar(response)
        # messages_list = list(response.context['messages'])
        # self.assertEqual(len(messages_list), 1)
        # self.assertEqual(messages_list[0].level, messages.ERROR)
