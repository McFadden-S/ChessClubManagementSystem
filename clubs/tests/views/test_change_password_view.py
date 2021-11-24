from django.test import TestCase
from clubs.models import User,Club_Member
from clubs.forms import UserChangePasswordForm
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

# Used this from clucker project with some modifications
class userChangePasswordViewTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        Club_Member.objects.create(
            user=self.user,
        )
        self.url = reverse('change_password')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'new_password_confirmation': 'NewPassword123',
        }

    def test_change_password_url(self):
        self.assertEqual(self.url, '/change_password/')


    def test_get_change_password(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)


    def test_get_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_succesful_password_change(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post(self.url, self.form_input)
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_password_change_unsuccesful_without_correct_old_password(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_password_change_unsuccesful_without_password_confirmation(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['new_password_confirmation'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
        response1 = self.client.post(self.url, self.form_input)
        messages_list = list(response1.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_post_change_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
