"""Unit tests for the applicant list view."""
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester, NavbarTesterMixin, reverse_with_next
from django.test import TestCase
from django.urls import reverse


# Used this from clucker project with some modifications
class ApplicantListViewTestCase(TestCase, LogInTester, NavbarTesterMixin):
    """Unit tests for the applicant list view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.owner = User.objects.get(email='harrysmith@example.org')
        self.officer = User.objects.get(email='bobsmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
        self.applicant = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')

        Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        Club_Member.objects.create(
            user=self.member, authorization='ME', club=self.club
        )
        Club_Member.objects.create(
            user=self.applicant, authorization='AP', club=self.club
        )

        self.url = reverse('applicants_list', kwargs={'club_id': self.club.id})

    def test_applicants_list_url(self):
        """Test for the applicant list url."""
        self.assertEqual(self.url, f'/{self.club.id}/applicants_list/')

    """Unit tests for showing applicant list"""

    def test_get_applicants_list_by_owner(self):
        self.client.login(email=self.owner.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assert_main_navbar(response)
        self.assertTemplateUsed(response, 'applicants_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_applicants_list_by_officer(self):
        self.client.login(email=self.officer.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assert_main_navbar(response)
        self.assertTemplateUsed(response, 'applicants_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """Redirects"""

    def test_get_applicants_list_redirects_member_list_when_authorization_is_member(self):
        """Test for redirecting member to member list from applicant list"""
        self.client.login(email=self.member.email, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        # self.assert_main_navbar(response)
        redirect_url = reverse('members_list', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # WHEN LOGIN IS FIXED FOR APPLICANT
    # def test_get_applicants_list_redirects_member_list_when_authorization_is_APPLICANT(self):
    #     user1 = User.objects.create_user(email="a@example.com", first_name="a", last_name="a", chess_experience="BG",
    #                                      password='Password123')
    #     club1 = Club_Member.objects.create(user=user1, authorization='ME', club=self.club)
    #     self.client.login(email=user1.email, password='Password123')
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('dashboard')
    #     # ERROR MESSAGE
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_applicants_list_redirects_when_not_logged_in(self):
        """Test for redirecting when not logged in"""
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def create_ordered_list_by(self, order_by_var):
        """Test for creating ordered applicant list by var"""
        applicants_list = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
        sorted_list = User.objects.filter(id__in=applicants_list).order_by(order_by_var)
        return sorted_list

    # dont see any thing that uses get_all_users_except_applicants.
    # def test_all_members_but_applicants(self):
    #     ap_list = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
    #     members = User.objects.exclude(id__in=ap_list)
    #     return members
    #
    # def test_all_members(self):
    #     second_list = list(self.test_all_members_but_applicants())
    #     members1 = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
    #     members = list(User.objects.exclude(id__in=members1))
    #     self.assertListEqual(second_list, members)

    # TODO Refactor tests to reflect javascript search/sort
    # def test_sorted_list_first_name(self):
    #     sort_table = 'first_name'
    #     second_list = list(self.create_ordered_list_by(sort_table))
    #     self.client.login(email=self.officer.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     response = self.client.post(self.url, {'sort_table': sort_table})
    #     applicants_list = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
    #     applicants = list(User.objects.filter(id__in=applicants_list))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertListEqual(applicants, second_list)
    #
    # def test_sorted_list_last_name(self):
    #     sort_table = 'last_name'
    #     second_list = list(self.create_ordered_list_by(sort_table))
    #     self.client.login(email=self.officer.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     response = self.client.post(self.url, {'sort_table': sort_table})
    #     applicants_list = Club_Member.objects.filter(authorization='AP').values_list('user__id', flat=True)
    #     applicants = list(User.objects.filter(id__in=applicants_list))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertListEqual(applicants, second_list)
    #
    # def test_search_bar_to_filter_list(self):
    #     self.client.login(email=self.officer.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertContains(response, 'John Smith')
    #     self.assertContains(response, 'Beth Smith')
    #     search_bar = 'Beth'
    #     response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertContains(response, 'Beth Smith')
    #     self.assertNotContains(response, 'John Smith')
    #
    # def test_empty_search_bar(self):
    #     self.client.login(email=self.officer.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertContains(response, 'John Smith')
    #     self.assertContains(response, 'Beth Smith')
    #     search_bar = ''
    #     response = self.client.post(self.url, {'searched_letters': search_bar})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'applicants_list.html')
    #     self.assertContains(response, 'Beth Smith')
    #     self.assertContains(response, 'John Smith')
