from django.test import TestCase
from clubs.models import User, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

# Used this from clucker project with some modifications
class membersListViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.create(
            user=self.user, authorization='OW'
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


    #TODO Once Log In redirects to another view members only decorator and this test can be UNCOMMENTED
    # def test_get_members_list_redirects_when_applicant(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.club.authorization='AP'
    #     redirect_url = reverse_with_next('home', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
