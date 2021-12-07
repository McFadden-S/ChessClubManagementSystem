"""Tests of the transfer ownership view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester


class DemoteOfficerViewTestCase(TestCase, LogInTester):
    """Tests of the transfer ownership view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
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
        self.club.member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club
        )
        self.url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})

    def test_transfer_ownership_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/transfer_ownership/{self.officer.id}')

    def test_get_valid_transfer_ownership(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth1 = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth1, 'OW')
        auth2 = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth2, 'OF')

    def test_get_invalid_transfer_ownership(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response_url = self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        self.assertEqual(response_url.status_code, 200)
        auth1 = Club_Member.objects.get(user=self.officer).authorization
        self.assertNotEqual(auth1, 'OW')
        auth2 = Club_Member.objects.get(user=self.owner).authorization
        self.assertNotEqual(auth2, 'OF')

    def test_promote_invalid_applicant_with_owner(self):
        url = reverse('transfer_ownership', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        auth = Club_Member.objects.get(user=self.member).authorization
        self.assertNotEqual(auth, 'OF')

