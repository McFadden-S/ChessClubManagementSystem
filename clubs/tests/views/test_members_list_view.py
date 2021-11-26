from django.test import TestCase
from clubs.models import User, Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password


# Used this from clucker project with some modifications
class membersListViewTestCase(TestCase):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        self.tertiary_user = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_owner = Club_Member.objects.create(
            user=self.user, authorization='OW', club=self.club
        )
        Club_Member.objects.create(
            user=self.secondary_user, authorization='ME', club=self.club
        )
        Club_Member.objects.create(
            user=self.tertiary_user, authorization='ME', club=self.club
        )
        self.url = reverse('members_list')

    def create_ordered_list_by(self, order_by_var):
        member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)#.order_by('member.first_name')
        sorted_list = User.objects.filter(id__in=member_list).order_by(order_by_var)
        return sorted_list

    def test_members_list_url(self):
        self.assertEqual(self.url, '/members_list/')

    def test_get_members_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_members_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_members_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_search_bar_to_filter_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, 'John Smith')
        self.assertContains(response, 'Beth Smith')
        search_bar = 'Beth'
        response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, 'Beth Smith')
        self.assertNotContains(response, 'John Smith')

    def test_empty_search_bar(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, 'John Smith')
        self.assertContains(response, 'Beth Smith')
        search_bar = ''
        response = self.client.post(self.url, {'search_btn': True, 'searched_letters': search_bar})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, 'Beth Smith')
        self.assertContains(response, 'John Smith')

    def test_sorted_list_first_name(self):
        sort_table = 'first_name'
        second_list = list(self.create_ordered_list_by(sort_table))
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        response = self.client.post(self.url, {'sort_table': sort_table})
        member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)
        members = list(User.objects.filter(id__in=member_list))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertListEqual(members, second_list)

    def test_sorted_list_last_name(self):
        sort_table = 'last_name'
        second_list = list(self.create_ordered_list_by(sort_table))
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        response = self.client.post(self.url, {'sort_table': sort_table})
        member_list = Club_Member.objects.filter(authorization='ME').values_list('user__id', flat=True)
        members = list(User.objects.filter(id__in=member_list))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertListEqual(members, second_list)

    # TODO Once Log In redirects to another view members only decorator and this test can be UNCOMMENTED
    # def test_get_members_list_redirects_when_applicant(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.club.authorization='AP'
    #     redirect_url = reverse_with_next('home', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
