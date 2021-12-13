"""Tests of the apply club view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


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
        self.officer = User.objects.get(email='marrysmith@example.org')
        self.member = User.objects.get(email='harrysmith@example.org')
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)

        self.url = reverse('apply_club', kwargs={'club_id': self.club.id})

    def test_get_apply_club_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_apply_club_url(self):
        """Test for the apply club url."""

        self.assertEqual(self.url,f'/apply_club/{self.club.id}')

    def test_get_user_apply_club(self):
        """Test for user successfully applying for a club"""

        self.client.login(email=self.user.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_applying = Club_Member.objects.get(user=self.user).authorization
        self.assertEqual(auth_after_applying, 'AP')

    def test_get_owner_apply_same_club(self):
        """Test for owner trying to apply for the same club."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth, 'OW')

    def test_get_officer_apply_same_club(self):
        """Test for officer trying to apply for the same club."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth, 'OF')

    def test_get_member_apply_same_club(self):
        """Test for member trying to apply for the same club."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth, 'ME')

    def test_get_applicant_apply_same_club(self):
        """Test for applicant trying to apply for the same club."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth, 'AP')
