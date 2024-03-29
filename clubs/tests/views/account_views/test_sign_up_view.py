"""Unit tests for the sign up view."""
from clubs.forms import SignUpForm
from clubs.models import Club, Club_Member, User
from clubs.tests.helpers import LogInTester
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from with_asserts.mixin import AssertHTMLMixin


class SignUpViewTestCase(TestCase, LogInTester, AssertHTMLMixin):
    """Unit tests for the sign up view."""

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
        """Test for the sign-up url."""

        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        """Test for getting the sign up page"""

        response = self.client.get(self.url)
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertEqual(form.is_bound, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertFalse(self._is_logged_in())
        with self.assertHTML(response) as html:
            follow_signup_url = reverse('sign_up')
            button = html.find(f'.//form[@action="{follow_signup_url}"]/ul/li/input')
            gravatar_text = html.find(f'.//div[@class="card-body"]/p')
            gravatar_link_text = html.find(f'.//div[@class="card-body"]/p/a')
            header = html.find(f'.//div[@class="card-header"]/h1')
            log_in_text = html.find(f'.//div[@class="card-footer"]/p/a')
            self.assertEqual(button.value, "Sign Up")
            self.assertEquals(gravatar_text.text,
                              "To have a profile photo, sign up with a gravatar associated email or set up a gravatar ")
            self.assertEquals(gravatar_link_text.text, "here")
            self.assertEqual(header.text, "Sign Up")
            self.assertEqual(log_in_text.text, "here")

    def test_successful_sign_up(self):
        """Test for user successfully signing up """

        before_count = User.objects.count()
        before_count_club = Club_Member.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
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
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_unsuccessful_sign_up(self):
        """Test for user unsuccessfully signing up """

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

    """Unit tests for different authorisations in a club trying to access sign-up"""

    def test_get_sign_up_redirects_when_logged_in_as_applicant(self):
        self.client.login(email=self.applicant.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_get_sign_up_redirects_when_logged_in_as_member(self):
        self.client.login(email=self.member.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_sign_up_redirects_when_logged_in_as_officer(self):
        self.client.login(email=self.officer.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_sign_up_redirects_when_logged_in_as_owner(self):
        self.client.login(email=self.owner.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('members_list', kwargs={'club_id': self.club.id}))
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """Unit tests for different authorisations in a club trying to post sign-up form"""

    def test_post_signup_redirects_when_logged_in_as_applicant(self):
        self.client.login(email=self.applicant.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('show_club', kwargs={'club_id': self.club.id}), follow=True)
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_post_signup_redirects_when_logged_in_as_member(self):
        self.client.login(email=self.member.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('show_club', kwargs={'club_id': self.club.id}), follow=True)
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_post_signup_redirects_when_logged_in_as_officer(self):
        self.client.login(email=self.officer.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('show_club', kwargs={'club_id': self.club.id}), follow=True)
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_post_signup_redirects_when_logged_in_as_owner(self):
        self.client.login(email=self.owner.email, password="Password123")
        self.assertTrue(self._is_logged_in())
        self.client.get(reverse('show_club', kwargs={'club_id': self.club.id}), follow=True)
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """Unit tests for unsuccessful sign-up via password combinations"""

    def test_unsuccessful_sign_up_by_matching_invalid_passwords(self):
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

    def test_unsuccessful_sign_up_by_non_matching_invalid_passwords(self):
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

    def test_unsuccessful_sign_up_by_non_matching_valid_passwords(self):
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

    def test_unsuccessful_sign_up_by_using_email_taken_by_another_user(self):
        """ Test unsuccessful sign up via email already taken"""

        response1 = self.client.post(self.url, self.valid_form_input)
        after_count1 = User.objects.count()
        valid_form_input2 = {
            'email': 'bellasmith@example.org',
            'first_name': 'Peter',
            'last_name': 'Smith',
            'bio': 'Hi',
            'chess_experience': 'BG',
            'personal_statement': 'I am Orangutan',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.client.logout()
        response2 = self.client.post(self.url, valid_form_input2)
        after_count2 = User.objects.count()
        self.assertEqual(after_count2, after_count1)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'sign_up.html')
        form = response2.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
