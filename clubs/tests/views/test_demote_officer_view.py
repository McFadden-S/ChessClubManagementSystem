"""Tests of the demote officer view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class DemoteOfficerViewTestCase(TestCase, LogInTester):
    """Tests of the demote officer view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_owner = Club_Member.objects.create(
            user=self.owner,
            authorization='OW',
            club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer,
            authorization='OF',
            club=self.club
        )
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})

    def test_demote_officer_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/demote_officer/{self.officer.id}')

    def test_get_demote_valid_officer(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth, 'ME')
        response1 = self.client.get(self.url)

    def test_get_demote_invalid_officer(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response_url = self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        self.assertEqual(response_url.status_code, 200)
        auth = self.club_officer.authorization
        self.assertNotEqual(auth, "ME")

    def test_get_demote_officer_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
