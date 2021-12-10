"""Tests of the leave club view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester,reverse_with_next
from django.core.exceptions import ObjectDoesNotExist


class LeaveClubViewTestCase(TestCase, LogInTester):
    """Tests of the leave club view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.applicant = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.officer = User.objects.get(email='harrysmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_owner = Club_Member.objects.create(
            user=self.owner,
            authorization='OW',
            club=self.club
        )
        self.club_applicant = Club_Member.objects.create(
            user=self.applicant,
            authorization='AP',
            club=self.club
        )
        self.club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer,
            authorization='OF',
            club=self.club
        )
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.member.id})

    def test_leave_club_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/leave_club/{self.member.id}')

    def test_get_member_leave_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the member has left the club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)

    def test_get_officer_leave_club(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the officer has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the officer has left the club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.officer, club=self.club)

    def test_get_applicant_leave_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks whether if the applicant has left the club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user is not allowed to leave the club as applicant')

    def test_get_owner_leave_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks whether if the owner has left the club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The owner is not allowed to leave the club')

    def test_get_leave_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
