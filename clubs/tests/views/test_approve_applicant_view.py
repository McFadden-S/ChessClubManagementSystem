"""Unit tests for the approve applicant view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.test import TestCase
from django.urls import reverse

# Used this from clucker project with some modifications

class ApproveApplicantTestCase(TestCase, LogInTester):
    """Unit tests for the approve applicant view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='bobsmith@example.org')
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.member = User.objects.get(email="harrysmith@example.org")
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.another_officer = User.objects.get(email='marrysmith@example.org')
        self.another_member = User.objects.get(email='jamessmith@example.org')
        self.another_applicant = User.objects.get(email='kellysmith@example.org')

        Club_Member.objects.create(user=self.owner, authorization='OW', club=self.club)
        Club_Member.objects.create(user=self.officer, authorization='OF', club=self.club)
        Club_Member.objects.create(user=self.member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.applicant, authorization='AP',club=self.club)
        Club_Member.objects.create(user=self.another_officer, authorization='OF',club=self.club)
        Club_Member.objects.create(user=self.another_member, authorization='ME', club=self.club)
        Club_Member.objects.create(user=self.another_applicant, authorization='AP',club=self.club)

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id})

    def test_approve_applicant_url(self):
        """Test for the approve applicant url."""

        self.assertEqual(self.url, f'/{self.club.id}/approve_applicant/{self.applicant.id}')

    def test_get_approve_applicant_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in."""

        self.assertFalse(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'AP')

    def test_approve_applicant_with_owner(self):
        """Test for the owner successfully approving an applicant."""

        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_applicant_with_officer(self):
        """Test for the officer successfully approving an applicant."""

        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_applicant_with_member(self):
        """Test for the member not being able to approve an applicant."""

        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'AP')

    def test_approve_applicant_with_another_applicant(self):
        """Test for another applicant not being able to approve an applicant."""

        self.client.login(email=self.another_applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'AP')

    def test_approve_applicant_with_themselves(self):
        """Test for the applicant not being able to approve themselves."""

        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_before_approve, 'AP')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.applicant).authorization
        self.assertEqual(auth_after_approve, 'AP')

    def test_approve_member_with_owner(self):
        """Test for the owner not being able to approve a member."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_approve, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_member_with_officer(self):
        """Test for the officer not being able to approve a member."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_approve, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_member_with_another_member(self):
        """Test for another member not being able to approve a member."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
        self.client.login(email=self.another_member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_approve, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_member_with_applicant(self):
        """Test for the applicant not being able to approve a member."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_approve, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_member_with_themselves(self):
        """Test for the member not being able to approve themselves."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.member.id})
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_before_approve, 'ME')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.member).authorization
        self.assertEqual(auth_after_approve, 'ME')

    def test_approve_officer_with_owner(self):
        """Test for the owner not being able to approve an officer."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.officer.id})
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_approve, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_approve, 'OF')

    def test_approve_officer_with_another_officer(self):
        """Test for another officer not being able to approve an officer."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.officer.id})
        self.client.login(email=self.another_officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_approve, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_approve, 'OF')

    def test_approve_officer_with_member(self):
        """Test for the member not being able to approve an officer."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.officer.id})
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_approve, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_approve, 'OF')

    def test_approve_officer_with_applicant(self):
        """Test for the applicant not being able to approve an officer."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.officer.id})
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_approve, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_approve, 'OF')

    def test_approve_officer_with_themselves(self):
        """Test for the officer not being able to approve themselves."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.officer.id})
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_before_approve, 'OF')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.officer).authorization
        self.assertEqual(auth_after_approve, 'OF')

    def test_approve_owner_with_officer(self):
        """Test for the officer not being able to approve an owner."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.owner.id})
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_approve, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_approve, 'OW')

    def test_approve_owner_with_member(self):
        """Test for the member not being able to approve an owner."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.owner.id})
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_approve, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_approve, 'OW')

    def test_approve_owner_with_applicant(self):
        """Test for the applicant not being able to approve an owner."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.owner.id})
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_approve, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_approve, 'OW')

    def test_approve_owner_with_themselves(self):
        """Test for the owner not being able to approve themselves."""

        self.url = reverse('approve_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.owner.id})
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        auth_before_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_before_approve, 'OW')
        response = self.client.get(self.url)
        redirect_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        auth_after_approve = Club_Member.objects.get(user=self.owner).authorization
        self.assertEqual(auth_after_approve, 'OW')
