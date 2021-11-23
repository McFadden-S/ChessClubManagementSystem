"""Tests of the promote member view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member
from .helpers import LogInTester


class PromoteMemberViewTestCase(TestCase, LogInTester):
    """Tests of the promote member view."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email='johndoe@example.org',
            first_name='John',
            last_name='Doe',
            bio='Hello, I am John Doe.',
            password='Password123',
            is_active=True,
        )
        self.member = User.objects.create_user(
            email='janedoe@example.org',
            first_name='Jane',
            last_name='Doe',
            bio='Hello, I am Jane Doe.',
            password='Password123',
            is_active=True,
        )
        self.club_owner = Club_Member.objects.create(
            user=self.owner,
            authorization='OW'
        )
        self.club_member = Club_Member.objects.create(
            user=self.member,
            authorization='ME'
        )
        self.url = reverse('promote_member', kwargs={'member_id': self.member.id})

        

    def test_promote_member_url(self):
        self.assertEqual(self.url,f'/promote_member/{self.member.id}')

    def test_get_promote_valid_member(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        url = reverse('members_list')
        self.assertRedirects(response, url, status_code=302, target_status_code=200)
        auth = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth, 'OF')
    
    def test_get_promote_invalid_member(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response_url = self.client.get(reverse('members_list'))
        self.assertEqual(response_url.status_code, 200)
        auth = self.club_member.authorization
        self.assertNotEqual(auth, "OF")