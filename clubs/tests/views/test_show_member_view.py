""" Tests for show member"""
from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password
from clubs.tests.helpers import LogInTester
from django.contrib import messages

# Used this from clucker project with some modifications
class ShowMemberViewTestCase(TestCase, LogInTester):
    """ Tests for show member"""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/other_clubs.json'

    ]

    def setUp(self):
        self.club = Club.objects.get(name='Flying Orangutans')

        self.applicant = User.objects.get(email='kellysmith@example.org')
        self.club_applicant = Club_Member.objects.create(user=self.applicant,authorization="AP", club=self.club)

        self.owner = User.objects.get(email='bobsmith@example.org')
        self.club_owner = Club_Member.objects.create( user=self.owner, authorization='OW', club=self.club)

        self.officer = User.objects.get(email='bethsmith@example.org')
        self.officer_club = Club_Member.objects.create(user=self.officer, authorization="OF", club=self.club)

        self.member = User.objects.get(email='jamessmith@example.org')
        self.club_member = Club_Member.objects.create(user=self.member, authorization="ME", club=self.club)

        self.different_applicant = User.objects.get(email='bobjone@example.org')
        self.different_club = Club.objects.get(name='Flying Orangutans 2')
        self.different_club_applicant = Club_Member.objects.create(user=self.different_applicant , authorization="AP", club=self.different_club)

        self.target_user = User.objects.get(email='jamessmith@example.org')
        self.url = reverse('show_member', kwargs={'club_id' : self.club.id, 'member_id': self.target_user.id})

    def test_show_member_url(self):
        self.assertEqual(self.url, f'/{self.club.id}/show_member/{self.target_user.id}')

    def test_get_show_member_by_owner_in_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_member_by_officer_in_club(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_member_by_members_own_profile_in_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_member_by_member_who_looks_at_another_member_in_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        member2 = User.objects.get(email='marrysmith@example.org')
        club_member2 = Club_Member.objects.create(user=member2, authorization="ME", club=self.club)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_show_member_by_applicant_in_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.applicant.email)
        url1 = reverse('show_member', kwargs={'club_id': self.club.id, 'member_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('waiting_list', kwargs={'club_id' : self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'waiting_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_owner_cannot_access_another_member_profile_in_different_club(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_member', kwargs={'club_id': self.different_club.id, 'member_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_officer_cannot_access_another_member_profile_in_different_club(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_member', kwargs={'club_id': self.different_club.id, 'member_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_applicant_cannot_access_another_member_show_member_profile_in_different_club(self):
        self.client.login(email=self.applicant.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_member', kwargs={'club_id': self.different_club.id, 'member_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_member_cannot_access_another_member_profile_in_different_club(self):
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        target_user1 = User.objects.get(email=self.different_applicant.email)
        url1 = reverse('show_member', kwargs={'club_id': self.different_club.id, 'member_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_get_show_member_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())


    def test_post_show_member_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_get_show_member_with_valid_id(self):
        self.client.login(username=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member.html')
        self.assertContains(response, "James Smith")

    def test_get_show_member_with_invalid_id(self):
        self.client.login(username=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        url = reverse('show_member', kwargs={'club_id': self.club.id, 'member_id': self.owner.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('members_list', kwargs={'club_id' : self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')
