"""Tests of the create club view."""
from django.test import TestCase
from clubs.models import User, Club_Member, Club
from clubs.forms import CreateClubForm
from django.urls import reverse
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.contrib import messages
from with_asserts.mixin import AssertHTMLMixin

class CreateClubViewTestCase(TestCase, LogInTester, AssertHTMLMixin):
    """Tests of the create club view."""
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.secondary_user = User.objects.get(email='bethsmith@example.org')
        self.club = Club.objects.get(name='Flying Orangutans')
        Club_Member.objects.create(
            user=self.user, authorization='ME', club=self.club
        )
        Club_Member.objects.create(
            user=self.secondary_user, authorization='AP', club=self.club
        )
        self.valid_form_input = {
            'name': 'Orangutan',
            'address': 'Bush House',
            'city': 'London',
            'postal_code': 'WC2B 4BG',
            'country': 'GB',
            'description' : 'Aim to get the best orangutans out there'
        }
        self.invalid_form_input = {
            'name': 'Invalid Orangutan',
            'address': 'Bush ',
            'city': 'Ldn',
            'postal_code': 'WC2B 4BG',
            'country': 'GB',
            'description': 'Aim to get the worst orangutans out there'
        }
        self.url = reverse('create_club')

    def test_create_club_url(self):
        self.assertEqual(self.url,'/create_club/')

    def test_get_create_club_by_any_user_when_logged_ini(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,CreateClubForm))
        self.assertEqual(form.is_bound, False)
        with self.assertHTML(response) as html:
            follow_create_club_url = reverse('create_club')
            button = html.find(f'.//form[@action="{follow_create_club_url }"]/ul/li/input')
            header = html.find(f'.//div[@class="card-header"]/h1')
            self.assertEqual(button.value, "Create Club")
            self.assertEqual(header.text, "Create Club")


    def test_succesful_create_club(self):
        #Test 1 - Save to db
        self.client.login(email=self.user.email, password='Password123')
        before_count = Club.objects.count()
        before_count_clubmember = Club_Member.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        after_count_clubmember = Club_Member.objects.count()
        self.assertEqual(after_count_clubmember, before_count_clubmember+1)
        # Test 2 - redirects
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        #Test 3 - Get club
        club = Club.objects.get(name='Orangutan')
        self.assertEqual(club.name, 'Orangutan')
        self.assertEqual(club.address, 'Bush House')
        self.assertEqual(club.city, 'London')
        self.assertEqual(club.postal_code, 'WC2B 4BG')
        self.assertEqual(club.country, 'GB')
        self.assertEqual(club.description, 'Aim to get the best orangutans out there')
        #Test 4 - Message
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        

    def test_unsuccesful_create_club(self):
         self.client.login(email=self.user.email, password='Password123')
         before_count_club = Club.objects.count()
         before_count_clubmember = Club_Member.objects.count()
         response = self.client.post(self.url, self.invalid_form_input, follow=True)
         after_count_club = Club.objects.count()
         self.assertEqual(after_count_club, before_count_club)
         after_count_clubmember = Club_Member.objects.count()
         self.assertEqual(after_count_clubmember, before_count_clubmember)
         response_url = reverse('create_club')
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'create_club.html')

    def test_get_create_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())

    def test_post_create_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertFalse(self._is_logged_in())
