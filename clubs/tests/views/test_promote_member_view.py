"""Tests of the promote member view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club_Member, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class PromoteMemberViewTestCase(TestCase, LogInTester):
    """Tests of the promote member view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='johnsmith@example.org')
        self.another_officer = User.objects.get(email='marrysmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
        self.another_member = User.objects.get(email='jamessmith@example.org')
        self.applicant = User.objects.get(email='harrysmith@example.org')
        self.another_applicant = User.objects.get(email='kellysmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF',club=self.club)
        Club_Member.objects.create(user=self.another_officer, authorization='OF',club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.another_member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP',club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP',club=self.club)
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.member.id})

    def test_promote_member_url(self):
        """Test for the promote member url."""

        self.assertEqual(self.url,f'/{self.club.id}/promote_member/{self.member.id}')

    def test_get_promote_member_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_get_owner_promote_member(self):
        """Test for the owner successfully promoting a member."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_officer_promote_member(self):
        """Test for the officer not being able to promote a member."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_another_member_promote_member(self):
        """Test for the a member not being able to promote a member."""

        self.client.login(email=self.another_member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_applicant_promote_member(self):
        """Test for the applicant not being able to promote a member."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_member_promote_themselves(self):
        """Test for the member not being able to promote themselves."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_owner_promote_officer(self):
        """Test for the owner not being able to promote an officer."""

        self.client.login(email=self.owner.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_another_officer_promote_officer(self):
        """Test for another officer not being able to promote an officer."""

        self.client.login(email=self.another_officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_member_promote_officer(self):
        """Test for the member not being able to promote an officer."""

        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_applicant_promote_officer(self):
        """Test for the applicant not being able to promote an officer."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_officer_promote_themselves(self):
        """Test for the officer not being able to promote themselves."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_owner_promote_applicant(self):
        """Test for the owner not being able to promote an applicant."""

        self.client.login(email=self.owner.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_officer_promote_applicant(self):
        """Test for officer not being able to promote an applicant."""

        self.client.login(email=self.officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_member_promote_applicant(self):
        """Test for the member not being able to promote an applicant."""

        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_another_applicant_promote_applicant(self):
        """Test for another applicant not being able to promote an applicant."""

        self.client.login(email=self.another_applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_applicant_promote_themselves(self):
        """Test for the applicant not being able to promote themselves."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_officer_promote_owner(self):
        """Test for officer not being able to promote an owner."""

        self.client.login(email=self.officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_member_promote_owner(self):
        """Test for the member not being able to promote an owner."""

        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_applicant_promote_owner(self):
        """Test for applicant not being able to promote an owner."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_owner_promote_themselves(self):
        """Test for the owner not being able to promote themselves."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')
