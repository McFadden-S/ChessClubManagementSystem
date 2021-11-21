from django.test import TestCase
from clubs.models import User, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

# Used this from clucker project with some modifications
class ApplicantListViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.create(
            user=self.user, authorization='OF'
        )
        self.url = reverse('applicants_list')

    def test_applicants_list_url(self):
        self.assertEqual(self.url, '/applicants_list/')

    def test_get_applicants_list(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # self.assertContains()
        self.assertTemplateUsed(response, 'applicants_list.html')

    def test_get_applicants_list_redirects_member_list_when_authorization_is_member(self):
        user1 = User.objects.create_user(email="a@example.com",first_name="a",last_name="a",chess_experience="BG",password='Password123')
        club1 = Club.objects.create(user=user1, authorization='ME')
        self.client.login(email=user1.email, password='Password123')
        response = self.client.get(self.url)
        redirect_url=reverse('members_list')
        # ERROR MESSAGE
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # WHEN LOGIN IS FIXED FOR APPLICANT
    # def test_get_applicants_list_redirects_member_list_when_authorization_is_APPLICANT(self):
    #     user1 = User.objects.create_user(email="a@example.com",first_name="a",last_name="a",chess_experience="BG",password='Password123')
    #     club1 = Club.objects.create(user=user1, authorization='ME')
    #     self.client.login(email=user1.email, password='Password123')
    #     response = self.client.get(self.url)
    #     redirect_url=reverse('members_list')
    #     # ERROR MESSAGE
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_applicants_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
