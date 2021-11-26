from django.test import TestCase
from clubs.models import User,Club_Member, Club
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib import messages

class ShowApplicantViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.applicant = User.objects.get(email='bobsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_applicant = Club_Member.objects.create(
            user=self.applicant,
            club=self.club
        )
        self.officer = User.objects.get(email='bethsmith@example.org')
        self.officer_club = Club_Member.objects.create(
            user=self.officer, authorization="OF", club=self.club
        )
        self.target_user = User.objects.get(email='bobsmith@example.org')
        self.url = reverse('show_applicant', kwargs={'club_id' : self.club.id, 'applicant_id': self.target_user.id})

    def test_show_applicant_url(self):
        self.assertEqual(self.url, f'/{self.club.id}/show_applicant/{self.target_user.id}')

    def test_get_show_applicant(self):
        self.client.login(email=self.officer.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_applicant.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "Hi")
        self.assertContains(response, "BG")
        self.assertContains(response, "I am Orangutan")
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)


    def test_get_show_applicant_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_applicant_redirects_having_been_already_approved(self):
        self.client.login(username=self.officer.email, password='Password123')
        user1 = User.objects.create_user(email="a@example.com",first_name="a",last_name="a",chess_experience="BG",password='Password123')
        club_member1 = Club_Member.objects.create(user=user1, authorization='ME', club=self.club)
        target_user1 = User.objects.get(email='a@example.com')
        url1 = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': target_user1.id})
        response = self.client.get(url1, follow=True)
        response_url = reverse('applicants_list', kwargs={'club_id' : self.club.id})
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
        url = reverse('show_applicant', kwargs={'club_id': self.club.id, 'applicant_id': self.applicant.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('applicants_list', kwargs={'club_id' : self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicants_list.html')
    # APPROVAL TEST NOT SURE- FUNCTIONAL MAYBE
