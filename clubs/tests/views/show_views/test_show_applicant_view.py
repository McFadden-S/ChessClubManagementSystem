"""Unit tests for show applicant view"""
from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next, LogInTester, NavbarTesterMixin
from django.contrib import messages


class ShowApplicantViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for show applicant view"""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.applicant = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_applicant = Club_Member.objects.create(user=self.applicant, authorization="AP", club=self.club)
        self.member = User.objects.get(email='jamessmith@example.org')
        self.club_member = Club_Member.objects.create(user=self.member, authorization="ME", club=self.club)
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.officer_club = Club_Member.objects.create(user=self.officer, authorization="OF", club=self.club)
        self.owner = User.objects.get(email='kellysmith@example.org')
        self.club_owner = Club_Member.objects.create(user=self.owner, authorization="OW", club=self.club)

        self.different_applicant = User.objects.get(email='bobjone@example.org')
        self.different_club = Club.objects.get(name='Flying Orangutans 2')
        self.different_club_applicant = Club_Member.objects.create(user=self.different_applicant, authorization="AP",
                                                                   club=self.different_club)

        self.target_user = User.objects.get(email='bobsmith@example.org')
        self.url = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.target_user.id})

    def test_show_applicant_url(self):
        """Test for the show applicant url"""

        self.assertEqual(self.url, f'/{self.club.id}/show_applicant/{self.target_user.id}')

    """Unit tests for getting the show applicant page"""

    def test_get_show_applicant_by_officer_in_club(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "Hi")
        self.assertContains(response, "BG")
        self.assertContains(response, "I am Orangutan")
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_applicant_by_owner_in_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "Hi")
        self.assertContains(response, "BG")
        self.assertContains(response, "I am Orangutan")
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_applicant_redirects_when_not_logged_in(self):
        """Test for redirecting user when not logged in"""

        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    """Unit tests if user tries to access show applicant when applicant is already approved"""

    def test_get_show_applicant_by_officer_redirects_having_been_already_approved(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        user1 = User.objects.create_user(email="a@example.com", first_name="a", last_name="a", chess_experience="BG",
                                         password='Password123')
        club_member1 = Club_Member.objects.create(user=user1, authorization='ME', club=self.club)
        target_user1 = User.objects.get(email='a@example.com')
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')

    def test_get_show_applicant_by_owner_redirects_having_been_already_approved(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        user1 = User.objects.create_user(email="a@example.com", first_name="a", last_name="a", chess_experience="BG",
                                         password='Password123')
        club_member1 = Club_Member.objects.create(user=user1, authorization='ME', club=self.club)
        target_user1 = User.objects.get(email='a@example.com')
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')

    """Unit tests for applicants and members in club not being able to access show applicant page"""

    def test_applicant_cannot_access_his_own_show_applicant_profile_in_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'waiting_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_applicant_cannot_access_another_applicants_show_applicant_profile_in_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        applicant2 = User.objects.get(email='harrysmith@example.org')
        club_applicant2 = Club_Member.objects.create(
            user=applicant2,
            club=self.club
        )
        target_user1 = User.objects.get(email=applicant2.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('waiting_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'waiting_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_member_cannot_access_another_applicant_profile_in_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    """Unit tests for users trying to access a applicant profile in a different club"""

    def test_owner_cannot_access_another_applicant_profile_in_different_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.different_club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assert_main_navbar(response)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_officer_cannot_access_another_applicant_profile_in_different_club(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.different_club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assert_main_navbar(response)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_applicant_cannot_access_another_applicants_show_applicant_profile_in_different_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.different_club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_member_cannot_access_another_applicant_profile_in_different_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_applicant', kwargs={'club_id': self.different_club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    """Unit tests to get show applicant with valid and invalid id"""

    def test_get_show_applicant_with_valid_id(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assert_main_navbar(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")

    def test_get_show_applicant_with_invalid_id(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        url = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id + 9999})
        response = self.client.get(url, follow=True)
        self.assert_main_navbar(response)
        response_url = reverse('applicants_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')
