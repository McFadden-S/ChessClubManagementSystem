"""Unit tests for the leave club view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse


class LeaveClubViewTestCase(TestCase, LogInTester):
    """Unit tests for the leave club view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='harrysmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.applicant = User.objects.get(email='bethsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.wrong_club = Club.objects.get(name='Flying Orangutans 2')

        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)

        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.member.id})

    def test_leave_club_url(self):
        """Test for the leave club url."""

        self.assertEqual(self.url,f'/{self.club.id}/leave_club/{self.member.id}')

    def test_get_leave_club_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_member_leave_club(self):
        """Test for a member successfully leaving a club."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the member does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)

    def test_get_officer_leave_club(self):
        """Test for an officer successfully leaving a club."""

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

        # Checks if the officer does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.officer, club=self.club)

    def test_get_applicant_leave_club(self):
        """Test for an applicant not being able to leave a club."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user is not allowed to leave the club as applicant')

    def test_get_owner_leave_club(self):
        """Test for an owner not being able to leave a club."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no owner has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the owner still exists in the Club
        try:
            Club_Member.objects.get(user=self.owner, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The owner is not allowed to leave the club')

    def test_get_member_leave_wrong_club(self):
        """Test for a member not being able to leave a club that the member is not in."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id, 'member_id': self.member.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if club members still stay the same
        self.assertEqual(before_count, after_count)

    def test_get_officer_leave_wrong_club(self):
        """Test for an officer not being able to leave a club that the officer is not in."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id, 'member_id': self.officer.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if club members still stay the same
        self.assertEqual(before_count, after_count)

    def test_get_applicant_leave_wrong_club(self):
        """Test for an applicant not being able to leave a club that the applicant is not in."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id, 'member_id': self.applicant.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if club members still stay the same
        self.assertEqual(before_count, after_count)

    def test_get_owner_leave_wrong_club(self):
        """Test for an owner not being able to leave a club that the owner is not in."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('leave_club', kwargs={'club_id': self.wrong_club.id, 'member_id': self.owner.id})
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('dashboard')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if club members still stay the same
        self.assertEqual(before_count, after_count)
