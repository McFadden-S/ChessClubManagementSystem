"""Tests of the reject applicant view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.core.exceptions import ObjectDoesNotExist

class RejectApplicantViewTestCase(TestCase, LogInTester):
    """Tests of the reject applicant view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='johnsmith@example.org')
        self.member = User.objects.get(email='harrysmith@example.org')
        self.applicant = User.objects.get(email='bethsmith@example.org')
        self.another_applicant = User.objects.get(email='jamessmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP', club=self.club)
        self.url = reverse('reject_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id})

    def test_reject_applicant_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/reject_applicant/{self.applicant.id}')

    def test_get_reject_applicant_redirects_when_not_logged_in(self):
        self.assertFalse(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    def test_get_owner_reject_applicant(self):
        """Test for the owner successfully reject an applicant"""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the applicant has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the applicant does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.applicant, club=self.club)

    def test_get_officer_reject_applicant(self):
        """Test for the officer successfully reject an applicant"""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the applicant has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks if the applicant does not exist in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.applicant, club=self.club)

    def test_get_member_reject_applicant(self):
        """Test for member not being able to reject an applicant."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        # Members will not be able to see applicants_list so they will be redirected to members_list
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')

    def test_get_another_applicant_reject_applicant(self):
        """Test for another applicant not being able to reject an applicant."""

        self.client.login(email=self.another_applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        # Applicants will not be able to see applicants_list so they will be redirected to waiting_list
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no applicant has been removed
        self.assertEqual(before_count, after_count)

        # Checks if the applicant still exists in the Club
        try:
            Club_Member.objects.get(user=self.applicant, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')
