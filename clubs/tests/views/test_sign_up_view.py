from django.test import TestCase
from clubs.models import User,Club_Member
from clubs.forms import SignUpForm
from django.urls import reverse
from django.contrib.auth.hashers import check_password

class SignUpViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(email='bobsmith@example.org')
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

    def test_get_the_signup_will_redirect_when_user_logged_in(self):
        club = Club_Member.objects.create(user=self.user)
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        url_redirect_after = reverse('members_list')
        self.assertRedirects(response, url_redirect_after, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')

    def test_post_signup_redirects_when_logged_in(self):
        club = Club_Member.objects.create(user=self.user)
        self.client.login(email=self.user.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.valid_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

        redirect_url = reverse('members_list')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'members_list.html')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertTrue(isinstance(form,SignUpForm))
        self.assertEqual(form.is_bound, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_unsuccesful_sign_up(self):
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
        # self.assertFalse(self._is_logged_in())

    def test_succesful_sign_up(self):
         # SAVE TO USER DB
         before_count = User.objects.count()
         before_count_club = Club_Member.objects.count()
         response = self.client.post(self.url, self.valid_form_input, follow=True)
         after_count = User.objects.count()
         self.assertEqual(after_count, before_count+1)

         # SAVE TO CLUB DB
         after_count_club = Club_Member.objects.count()
         self.assertEqual(after_count_club, before_count_club+1)

         # TEST 2 - REDIRECT SUCCESSFUL MUST MAKE FOLLOWS IN RESPONSE TRUE
         response_url = reverse('waiting_list')
         self.assertRedirects(response, response_url, status_code=302, target_status_code=200)


         self.assertTemplateUsed(response, 'waiting_list.html')

         #test 4 - IN DB SEE NEW USER
         user = User.objects.get(email='bobsmith@example.org')
         self.assertEqual(user.first_name, 'Bob')
         self.assertEqual(user.last_name, 'Smith')
         self.assertEqual(user.bio, 'Hi')
         # from django.contrib.auth.hashers import check_password
         is_password_correct = check_password('Password123', user.password)
         self.assertTrue(is_password_correct)
         # self.assertTrue(self._is_logged_in())
