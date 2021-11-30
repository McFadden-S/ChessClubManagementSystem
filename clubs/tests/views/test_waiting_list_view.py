from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password
from django.contrib import messages


# Used this from clucker project with some modifications
class ApplicantListViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        # this is the officer
        self.officer = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        self.tertiary_user = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_officer = Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        Club_Member.objects.create(
            user=self.secondary_user, authorization='AP', club=self.club
        )
        Club_Member.objects.create(
            user=self.tertiary_user, authorization='AP', club=self.club
        )
        self.owner = User.objects.get(email='harrysmith@example.org')
        Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.url = reverse('waiting_list', kwargs={'club_id': self.club.id})

    def test_applicants_list_url(self):
        self.assertEqual(self.url, f'/{self.club.id}/waiting_list/')

    def test_get_applicants_list_redirects_member_list_when_authorization_is_member(self):
        user1 = User.objects.create_user(email="a@example.com", first_name="a", last_name="a", chess_experience="BG",
                                         password='Password123')
        club_member1 = Club_Member.objects.create(user=user1, authorization='AP', club=self.club)
        self.client.login(email=user1.email, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertEqual(response.status_code, 200)
