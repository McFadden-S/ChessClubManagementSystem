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
        self.applicant = User.objects.get(email='bethsmith@example.org')
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
        self.url = reverse('reject_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id})

    def test_reject_applicant_url(self):
        self.assertEqual(self.url,f'/{self.club.id}/reject_applicant/{self.applicant.id}')

    def test_get_reject_applicant(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.url)
        url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the applicant has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the applicant still exists in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.applicant, club=self.club)

    def test_get_reject_applicant_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
