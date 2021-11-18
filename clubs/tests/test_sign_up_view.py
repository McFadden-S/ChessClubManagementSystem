from django.test import TestCase
from clubs.models import User
from clubs.forms import SignUpForm
from django.urls import reverse

class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='bobsmith@example.com',
            first_name = 'Bob',
            last_name = 'Smith',
            bio='Hi',
            chess_experience='AV',
            personal_statement = 'I am Orangutan',
            password="Orangutan123"
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

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertTrue(isinstance(form,SignUpForm))
        self.assertEqual(form.is_bound, False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
