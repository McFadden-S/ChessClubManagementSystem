"""Unit tests for the waiting list view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, NavbarTesterMixin,reverse_with_next
from django.contrib.auth.hashers import check_password
from django.contrib import messages

class WaitingListViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for the waiting list view."""
    
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
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

    """Unit tests for different authorisations in a club trying to access waiting list"""

    def test_get_waiting_list_when_users_club_authorisation_is_applicant(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'waiting_list.html')
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)

    def test_get_waiting_list_when_users_club_authorisation_is_member(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_waiting_list_redirects_to_members_list_when_users_club_authorisation_is_officer(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_waiting_list_redirects_to_members_list_when_users_club_authorisation_is_owner(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
