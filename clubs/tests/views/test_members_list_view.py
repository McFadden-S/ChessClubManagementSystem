from django.test import TestCase
from clubs.models import User, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

# Used this from clucker project with some modifications
class membersListViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/secondary_user.json',
        'clubs/tests/fixtures/tertiary_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        self.tertiary_user = User.objects.get(email='johnsmith@example.org')
        self.club = Club.objects.create(
            user=self.user, authorization='OW'
        )
        Club.objects.create(
            user=self.secondary_user, authorization='ME'
        )
        Club.objects.create(
            user=self.tertiary_user, authorization='ME'
        )
        self.url = reverse('members_list')

    def test_members_list_url(self):
        self.assertEqual(self.url, '/members_list/')

    def test_get_members_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')

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
        response = self.client.post(self.url, {'searched_letters': search_bar})
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
        response = self.client.post(self.url, {'searched_letters': search_bar})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members_list.html')
        self.assertContains(response, 'Beth Smith')
        self.assertContains(response, 'John Smith')


    #TODO Once Log In redirects to another view members only decorator and this test can be UNCOMMENTED
    # def test_get_members_list_redirects_when_applicant(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.club.authorization='AP'
    #     redirect_url = reverse_with_next('home', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
