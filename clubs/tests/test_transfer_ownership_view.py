"""Tests of the transfer ownership view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from .helpers import LogInTester


class DemoteOfficerViewTestCase(TestCase, LogInTester):
    """Tests of the transfer ownership view."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email='johndoe@example.org',
            first_name='John',
            last_name='Doe',
            bio='Hello, I am John Doe.',
            password='Password123',
            is_active=True,
        )
        self.officer = User.objects.create_user(
            email='janedoe@example.org',
            first_name='Jane',
            last_name='Doe',
            bio='Hello, I am Jane Doe.',
            password='Password123',
            is_active=True,
        )
        self.club_owner = Club.objects.create(
            user=self.owner,
            authorization='OW'
        )
        self.club_officer = Club.objects.create(
            user=self.officer,
            authorization='OF'
        )
        self.url = reverse('transfer_ownership', kwargs={'member_id': self.officer.id})

        

    def test_transfer_ownership_url(self):
        self.assertEqual(self.url,f'/transfer_ownership/{self.officer.id}')

    def test_get_valid_transfer_ownership(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('members_list')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth1 = Club.objects.get(user=self.officer).authorization
        self.assertEqual(auth1, 'OW')
        auth2 = Club.objects.get(user=self.owner).authorization
        self.assertEqual(auth2, 'OF')
    
    def test_get_invalid_transfer_ownership(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response_url = self.client.get(reverse('members_list'))
        self.assertEqual(response_url.status_code, 200)
        auth1 = Club.objects.get(user=self.officer).authorization
        self.assertNotEqual(auth1, 'OW')
        auth2 = Club.objects.get(user=self.owner).authorization
        self.assertNotEqual(auth2, 'OF')