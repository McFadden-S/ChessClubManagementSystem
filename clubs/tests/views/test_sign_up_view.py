from django.test import TestCase
from clubs.models import User, Club_Member, Club
from clubs.forms import SignUpForm
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from clubs.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):
    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.applicant = User.objects.get(email='bobsmith@example.org')
        self.member = User.objects.get(email='bethsmith@example.org')
        self.officer = User.objects.get(email='johnsmith@example.org')
        self.owner = User.objects.get(email='harrysmith@example.org')

        self.club = Club.objects.get(name='Flying Orangutans')
        self.club_applicant = Club_Member.objects.create(
            user=self.applicant, authorization='AP', club=self.club
        )
        self.club_member = Club_Member.objects.create(
            user=self.member, authorization='ME', club=self.club
        )
        self.club_officer = Club_Member.objects.create(
            user=self.officer, authorization='OF', club=self.club
        )
        self.club_owner = Club_Member.objects.create(
            user=self.owner, authorization='OW', club=self.club
        )
        self.valid_form_input = {
            'email': 'bellasmith@example.org',
            'first_name': 'Bella',
            'last_name': 'Smith',
            'bio': 'Hi',
            'chess_experience': 'BG',
            'personal_statement': 'I am Orangutan',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.url = reverse('sign_up')


    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertTrue(isinstance(form,SignUpForm))
        self.assertEqual(form.is_bound, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """ 1) Successful and unsuccessful signups"""
    def test_succesful_sign_up_by_applicant(self):
        before_count = User.objects.count()
        before_count_club = Club_Member.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        after_count_club = Club_Member.objects.count()
        self.assertEqual(after_count_club, before_count_club)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        user = User.objects.get(email='bellasmith@example.org')
        self.assertEqual(user.first_name, 'Bella')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.bio, 'Hi')
        self.assertEqual(user.chess_experience, 'BG')
        self.assertEqual(user.personal_statement, 'I am Orangutan')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccesful_sign_up_using_email_by_applicant(self):
        self.valid_form_input['email'] = '@yahoo.com'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    """ 2) Get sign-up redirect tests"""
    def test_get_sign_up_redirects_when_logged_in_as_applicant(self):
        self.client.login(email=self.applicant.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_sign_up_redirects_when_logged_in_as_member(self):
        self.client.login(email=self.member.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_sign_up_redirects_when_logged_in_as_officer(self):
        self.client.login(email=self.officer.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_sign_up_redirects_when_logged_in_as_owner(self):
        self.client.login(email=self.owner.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')


    """ 3) Post sign-up redirect tests"""
    def test_post_signup_redirects_when_logged_in_as_applicant(self):
        self.client.login(email=self.applicant.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_signup_redirects_when_logged_in_as_member(self):
        self.client.login(email=self.member.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_signup_redirects_when_logged_in_as_officer(self):
        self.client.login(email=self.officer.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_post_signup_redirects_when_logged_in_as_owner(self):
        self.client.login(email=self.owner.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        

    """ 4) Password combinations """
    def test_unsuccesful_sign_up_by_matching_invalid_passwords(self):
        self.valid_form_input['new_password'] = 'hello'
        self.valid_form_input['confirmation_password'] = 'hello'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_unsuccesful_sign_up_by_non_matching_invalid_passwords(self):
        self.valid_form_input['new_password'] = 'hello'
        self.valid_form_input['confirmation_password'] = 'hello123'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_unsuccesful_sign_up_by_non_matching_valid_passwords(self):
        self.valid_form_input['new_password'] = 'Orangutan123'
        self.valid_form_input['confirmation_password'] = 'Passwor123'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
