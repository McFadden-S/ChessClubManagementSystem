from django.test import TestCase
from clubs.models import User,Club_Member
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next

class ShowApplicantViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.club = Club_Member.objects.create(
            user=self.user
        )
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.officer_club = Club_Member.objects.create(
            user=self.officer, authorization="OF"
        )
        self.target_user = User.objects.get(email='bobsmith@example.org')
        self.url = reverse('show_applicant', kwargs={'applicant_id': self.target_user.id})

    def test_show_applicant_url(self):
        self.assertEqual(self.url, f'/show_applicant/{self.target_user.id}')

    def test_get_show_applicant(self):
        self.client.login(email=self.officer.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "Hi")
        self.assertContains(response, "BG")
        self.assertContains(response, "I am Orangutan")

    def test_get_show_applicant_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_applicant_redirects_having_been_already_approved(self):
        self.client.login(username=self.officer.email, password='Password123')
        user1 = User.objects.create_user(email="a@example.com",first_name="a",last_name="a",chess_experience="BG",password='Password123')
        club1 = Club_Member.objects.create(user=user1, authorization='ME')
        target_user1 = User.objects.get(email='a@example.com')
        url1 = reverse('show_applicant', kwargs={'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('applicants_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')


    def test_get_show_applicant_with_valid_id(self):
        self.client.login(username=self.officer.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")

    def test_get_show_applicant_with_invalid_id(self):
        self.client.login(username=self.officer.email, password='Password123')
        url = reverse('show_applicant', kwargs={'applicant_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('applicants_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')
    # APPROVAL TEST NOT SURE- FUNCTIONAL MAYBE
