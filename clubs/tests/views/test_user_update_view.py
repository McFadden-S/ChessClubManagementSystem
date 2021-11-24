from django.test import TestCase
from clubs.models import User
from clubs.forms import UserUpdateForm
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

# Used this from clucker project with some modifications
class userUpdateViewTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
        self.user2 = User.objects.get(email='bethsmith@example.org')
        self.url = reverse('update_user')
        self.form_input = {
            "first_name": "Boby",
            "last_name": "Smithy",
            "email": "bobysmithy@example.org",
            "bio": "Hiya",
            "chess_experience": "AV",
            "personal_statement": "I am Not Orangutan",
        }

    def test_user_update_url(self):
        self.assertEqual(self.url, '/update_user/')

    def test_get_user_update(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserUpdateForm))

    def test_get_user_update_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_user_update_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_succesful_user_update(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.first_name, self.form_input['first_name'])
        self.assertTrue(self.user.last_name, self.form_input['last_name'])
        self.assertTrue(self.user.email, self.form_input['email'])
        self.assertTrue(self.user.bio, self.form_input['bio'])
        self.assertTrue(self.user.chess_experience, self.form_input['chess_experience'])
        self.assertTrue(self.user.personal_statement, self.form_input['personal_statement'])

    def test_unsuccesful_user_update_with_blank_first_name(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['first_name'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserUpdateForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.first_name == '')

    def test_unsuccesful_user_update_with_blank_last_name(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['last_name'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserUpdateForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.last_name == '')

    def test_unsuccesful_user_update_with_incorrect_email(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = 'notemail'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserUpdateForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.email == 'notemail')

    def test_unsuccesful_user_update_with_duplicate_email(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = self.user2.email
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_update.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserUpdateForm))
        self.user.refresh_from_db()
        self.assertFalse(self.user.email == self.user2.email)
