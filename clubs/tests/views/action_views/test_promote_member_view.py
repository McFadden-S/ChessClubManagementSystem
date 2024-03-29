"""Unit tests for the promote member view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.test import TestCase
from django.urls import reverse
from django.contrib import messages


class PromoteMemberViewTestCase(TestCase, LogInTester):
    """Unit tests for the promote member view."""
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
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.another_officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.another_member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP', club=self.club)

        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.member.id})

    def test_promote_member_url(self):
        """Test for the promote member url."""

        self.assertEqual(self.url, f'/{self.club.id}/promote_member/{self.member.id}')

    def test_get_promote_member_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_owner_promote_member(self):
        """Test for the owner successfully promoting a member."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_promotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        response_message = self.client.get(redirect_url)
        messages_list = list(response_message.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    """Unit tests for user not being able to promote a member"""

    def test_get_officer_promote_member(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_promotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_another_member_promote_member(self):
        self.client.login(email=self.another_member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_promotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_applicant_promote_member(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_promotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    def test_get_member_promote_themselves(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_promotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_promotion, 'ME')

    """Unit tests for user not being able to promote an officer"""

    def test_get_owner_promote_officer(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_promotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_another_officer_promote_officer(self):
        self.client.login(email=self.another_officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_promotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_member_promote_officer(self):
        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_promotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_applicant_promote_officer(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_promotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    def test_get_officer_promote_themselves(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        auth_before_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_promotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_promotion, 'OF')

    """Unit tests for user not being able to promote an applicant"""

    def test_get_owner_promote_applicant(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_promotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_officer_promote_applicant(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_promotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_member_promote_applicant(self):
        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_promotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_another_applicant_promote_applicant(self):
        self.client.login(email=self.another_applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_promotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    def test_get_applicant_promote_themselves(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_promotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_promotion, 'AP')

    """Unit tests for user not being able to promote an owner"""

    def test_get_officer_promote_owner(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_promotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_member_promote_owner(self):
        self.client.login(email=self.member.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_promotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_applicant_promote_owner(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        self.assertTrue(self._is_logged_in())
        auth_before_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_promotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')

    def test_get_owner_promote_themselves(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('promote_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        auth_before_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_promotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_promotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_promotion, 'OW')
