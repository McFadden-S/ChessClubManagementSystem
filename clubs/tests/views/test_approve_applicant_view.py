from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next, LogInTester
from django.contrib.auth.hashers import check_password
from django.contrib import messages


# Used this from clucker project with some modifications

class ApproveApplicantTestCase(TestCase, LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.member = User.objects.get(email="harrysmith@example.org")
        self.club = Club.objects.get(name='Flying Orangutans')

        self.owner2 = User.objects.get(email='harrysmith@example.org')
        self.member2 = User.objects.get(email='bobsmith@example.org')
        self.club2 = Club.objects.create(
            # Broad St, Oxford OX1 3BG
            name='club2',
            address='Broad St',
            city='Oxford',
            postal_code='OX1 3BG	',
            country='United Kingdom',
            description='Bodleian Library',
        )

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
        self.club_applicant = Club_Member.objects.create(
            user=self.applicant,
            authorization='AP',
            club=self.club,
        )
        self.club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club,
        )

        self.club_owner2 = Club_Member.objects.create(
            user=self.owner2,
            authorization='OW',
            club=self.club2
        )

        self.club_member2 = Club_Member.objects.create(
            user=self.member2,
            authorization='ME',
            club=self.club2,
        )

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id})

    def test_approve_applicant_url(self):
        self.assertEqual(self.url, f'/{self.club.id}/approve_applicant/{self.applicant.id}')

    def test_approve_valid_applicant_with_owner(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth, 'ME')

    # fix when applicants is initialise in views.
    # def test_approve_valid_applicant_with_officer(self):
    #     self.client.login(email='bethsmith@example.org', password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     auth = Club_Member.objects.get(user=self.applicant).authorization
    #     self.assertEqual(auth, 'AP')
    #     response = self.client.get(self.url)
    #     url = reverse('applicants_list', kwargs={'club_id': self.club.id})
    #     self.assertRedirects(response, url, status_code=302, target_status_code=200)
    #     auth = Club_Member.objects.get(user=self.applicant).authorization
    #     self.assertEqual(auth, 'ME')

    # def test_approve_invalid_applicant_with_owner(self):
    #     url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
    #     self.client.login(email='bobsmith@example.org', password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     response = self.client.get(url)
    #     url = reverse('applicants_list', kwargs={'club_id': self.club.id})
    #     self.assertRedirects(response, url, status_code=302, target_status_code=200)
    #     auth = Club_Member.objects.get(user=self.member).authorization
    #     self.assertEqual(auth, 'ME')
