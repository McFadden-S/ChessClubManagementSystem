"""Tests of the remove user view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester
from django.core.exceptions import ObjectDoesNotExist

class RemoveUserViewTestCase(TestCase, LogInTester):
    """Tests of the remove user view."""
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
        self.club_member = Club_Member.objects.create(
            user=self.officer,
            authorization='OF',
            club=self.club
        )
        self.club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME',
            club=self.club
        )
        self.remove_member_url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.member.id})
        self.remove_officer_url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.officer.id})

    def test_remove_member_url(self):
        self.assertEqual(self.remove_member_url,f'/{self.club.id}/remove_user/{self.member.id}')

    def test_remove_officer_url(self):
        self.assertEqual(self.remove_officer_url,f'/{self.club.id}/remove_user/{self.officer.id}')

    def test_get_owner_remove_member(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the member still exists in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)

    def test_get_owner_remove_officer(self):
        self.client.login(email='bobsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_officer_url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the member still exists in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.officer, club=self.club)

    def test_get_officer_remove_member(self):
        self.client.login(email='bethsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        response = self.client.get(self.remove_member_url)
        url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if the member has been removed
        self.assertEqual(before_count, after_count+1)

        # Checks whether if the member still exists in the Club
        with self.assertRaises(ObjectDoesNotExist):
            Club_Member.objects.get(user=self.member, club=self.club)

    def test_get_invalid_remove_user(self):
        self.client.login(email='bethsmith@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Club_Member.objects.count()
        url = reverse('remove_user', kwargs={'club_id': self.club.id, 'user_id': self.owner.id})
        response = self.client.get(url)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = Club_Member.objects.count()
        # Checks if no user has been removed
        self.assertEqual(before_count, after_count)

        # Checks whether if the user still exists in the Club
        try:
            Club_Member.objects.get(user=self.officer, club=self.club)
        except (ObjectDoesNotExist):
            self.fail('The user should not be removed')
