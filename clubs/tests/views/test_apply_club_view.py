"""Tests of the apply club view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester


class ApplyClubViewTestCase(TestCase, LogInTester):
    """Tests of the apply club view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.user = User.objects.get(email='bethsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_owner = Club_Member.objects.create(
            user=self.owner,
            authorization='OW',
            club=self.club
        )
        self.url = reverse('apply_club', kwargs={'club_id': self.club.id})

    def test_apply_club_url(self):
        self.assertEqual(self.url,f'/apply_club/{self.club.id}')

    def test_get_user_apply_club(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('waiting_list.html')
        auth = Club_Member.objects.get(user=self.user).authorization
        self.assertEqual(auth, 'AP')

    def test_get_owner_apply_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth, 'OW')
