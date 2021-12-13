"""Unit tests for the demote officer view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.test import TestCase
from django.urls import reverse


class DemoteOfficerViewTestCase(TestCase, LogInTester):
    """Unit tests for the demote officer view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email='johnsmith@example.org')
        self.applicant = User.objects.get(email='harrysmith@example.org')
        self.another_officer = User.objects.get(email='marrysmith@example.org')
        self.another_member = User.objects.get(email='jamessmith@example.org')
        self.another_applicant = User.objects.get(email='kellysmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP', club=self.club)
        Club_Member.objects.create(user=self.another_officer, authorization='OF',club=self.club)
        Club_Member.objects.create(user=self.another_member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP',club=self.club)

        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})

    def test_demote_officer_url(self):
        """Test for the demote officer url."""

        self.assertEqual(self.url,f'/{self.club.id}/demote_officer/{self.officer.id}')

    def test_get_demote_officer_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'OF')

    def test_get_owner_demote_officer(self):
        """Test for the owner successfully demoting an officer."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'ME')

    def test_get_owner_demote_member(self):
        """Test for the owner not being able to demote a member."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        auth_before_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_demotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_demotion, 'ME')

    def test_get_owner_demote_applicant(self):
        """Test for the owner not being able to demote an applicant."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_demotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_demotion, 'AP')

    def test_get_owner_demote_themselves(self):
        """Test for the owner not being able to demote themselves."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        auth_before_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_demotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_demotion, 'OW')

    def test_get_officer_demote_owner(self):
        """Test for the officer not being able to demote an owner."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        auth_before_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_demotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_demotion, 'OW')

    def test_get_another_officer_demote_officer(self):
        """Test for another officer not being able to demote an officer."""

        self.client.login(email=self.another_officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'OF')

    def test_get_officer_demote_member(self):
        """Test for the officer not being able to demote a member."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        auth_before_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_demotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_demotion, 'ME')

    def test_get_officer_demote_applicant(self):
        """Test for the officer not being able to demote an applicant."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_demotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_demotion, 'AP')

    def test_get_officer_demote_themselves(self):
        """Test for the officer not being able to demote themselves."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.officer.id})
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'OF')

    def test_get_member_demote_owner(self):
        """Test for the member not being able to demote an owner."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        auth_before_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_demotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_demotion, 'OW')

    def test_get_member_demote_officer(self):
        """Test for member not being able to demote an officer."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'OF')

    def test_get_another_member_demote_member(self):
        """Test for another member not being able to demote a member."""

        self.client.login(email=self.another_member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        auth_before_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_demotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_demotion, 'ME')

    def test_get_member_demote_applicant(self):
        """Test for the member not being able to demote an applicant."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_demotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_demotion, 'AP')

    def test_get_member_demote_themselves(self):
        """Test for the member not being able to demote themselves."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        auth_before_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_demotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_demotion, 'ME')


    def test_get_applicant_demote_owner(self):
        """Test for the applicant not being able to demote an owner."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.owner.id})
        auth_before_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_demotion, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_demotion, 'OW')

    def test_get_applicant_demote_officer(self):
        """Test for applicant not being able to demote an officer."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_demotion, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_demotion, 'OF')

    def test_get_applicant_demote_member(self):
        """Test for the applicant not being able to demote a member."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.member.id})
        auth_before_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_demotion, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_demotion, 'ME')

    def test_get_another_applicant_demote_applicant(self):
        """Test for another applicant not being able to demote an applicant."""

        self.client.login(email=self.another_applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_demotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_demotion, 'AP')

    def test_get_applicant_demote_themselves(self):
        """Test for the applicant not being able to demote themselves."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.url = reverse('demote_officer', kwargs={'club_id': self.club.id, 'member_id': self.applicant.id})
        auth_before_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_demotion, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_demotion = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_demotion, 'AP')
