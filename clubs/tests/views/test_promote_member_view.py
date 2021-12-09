"""Tests of the promote member view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class PromoteMemberViewTestCase(TestCase, LogInTester):
    """Tests of the promote member view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='johnsmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
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
        self.club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club
        )
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.member.id})

    def test_promote_member_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/promote_member/{self.member.id}')

    def test_get_promote_valid_member(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth, 'OF')

    def test_get_promote_invalid_member(self):
        self.client.login(email='bethsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        self.assertEqual(response.status_code, 200)
        auth = self.club_member.authorization
        self.assertNotEqual(auth, "OF")

    def test_promote_invalid_applicant_with_owner(self):
        url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        auth = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth, 'OF')

    def test_get_promote_member_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
