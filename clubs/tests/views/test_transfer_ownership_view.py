"""Tests of the transfer ownership view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.core.exceptions import ObjectDoesNotExist

class DemoteOfficerViewTestCase(TestCase, LogInTester):
    """Tests of the transfer ownership view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.applicant = User.objects.get(email='harrysmith@example.org')
        self.user_from_other_club = User.objects.get(email='marrysmith@example.org')
        self.clubless_user = User.objects.get(email='kellysmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.other_club = Club.objects.get(name='Flying Orangutans 2')

        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)
        Club_Member.objects.create(user=self.user_from_other_club, authorization='OF', club=self.other_club)

        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})

    def test_transfer_ownership_url(self):
        """Test for the transfer ownership url."""

        self.assertEqual(self.url,f'/{self.club.id}/transfer_ownership/{self.officer.id}')

    def test_get_transfer_ownership_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_owner_transfer_ownership_to_officer(self):
        """Test for the owner successfully transferring ownership to an officer."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        owner_auth_after_transfer = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(owner_auth_after_transfer, 'OF')
        officer_auth_after_transfer = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(officer_auth_after_transfer, 'OW')

    """Unit tests for not being able to transfer ownership"""

    def test_get_owner_transfer_ownership_to_member(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        owner_auth_after_transfer = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(owner_auth_after_transfer, 'OW')
        member_auth_after_transfer = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(member_auth_after_transfer, 'ME')

    def test_get_owner_transfer_ownership_to_applicant(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        owner_auth_after_transfer = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(owner_auth_after_transfer, 'OW')
        applicant_auth_after_transfer = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(applicant_auth_after_transfer, 'AP')

    def test_get_owner_transfer_ownership_to_user_from_other_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.user_from_other_club.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        owner_auth_after_transfer = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(owner_auth_after_transfer, 'OW')
        user_from_other_club_auth_after_transfer = Club_Member.objects.get(user=self.user_from_other_club).authorization
        self.assertEqual(user_from_other_club_auth_after_transfer, 'OF')

    def test_get_owner_transfer_ownership_to_clubless_user(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.clubless_user.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        owner_auth_after_transfer = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(owner_auth_after_transfer, 'OW')
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.clubless_user, club=self.club)
